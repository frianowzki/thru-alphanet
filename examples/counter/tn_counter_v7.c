#include <stddef.h>
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>
#include "tn_counter_v7.h"

static void handle_create_counter(uchar const *instruction_data, ulong instruction_data_sz TSDK_PARAM_UNUSED) {
    tn_counter_create_args_t const *args = (tn_counter_create_args_t const *)instruction_data;
    ushort account_idx = args->account_index;

    /* Get proof data pointer (follows the struct) */
    uchar const *proof_data = NULL;
    if (args->proof_size > 0) {
        proof_data = instruction_data + sizeof(tn_counter_create_args_t);
    }

    /* Create the account */
    ulong result = tsys_account_create(account_idx, args->counter_program_seed, proof_data, args->proof_size);
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_CREATE_FAILED);
    }

    /* Set account as writable */
    result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_SET_WRITABLE_FAILED);
    }

    /* Resize account to hold counter data */
    result = tsys_account_resize(account_idx, sizeof(tn_counter_account_t));
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_RESIZE_FAILED);
    }

    /* Initialize counter to 0 */
    tn_counter_account_t *counter = (tn_counter_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (counter == NULL) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_DATA_ACCESS_FAILED);
    }
    counter->counter_value = 0UL;

    tsdk_return(TSDK_SUCCESS);
}

static void handle_increment(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_SET_WRITABLE_FAILED);
    }

    tn_counter_account_t *counter = (tn_counter_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (counter == NULL) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_DATA_ACCESS_FAILED);
    }

    counter->counter_value++;
    tsys_emit_event((uchar const *)&counter->counter_value, sizeof(ulong));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_decrement(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_SET_WRITABLE_FAILED);
    }

    tn_counter_account_t *counter = (tn_counter_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (counter == NULL) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_DATA_ACCESS_FAILED);
    }

    /* Underflow protection */
    if (counter->counter_value == 0UL) {
        tsdk_revert(TN_COUNTER_ERR_COUNTER_UNDERFLOW);
    }

    counter->counter_value--;
    tsys_emit_event((uchar const *)&counter->counter_value, sizeof(ulong));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_reset(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_SET_WRITABLE_FAILED);
    }

    tn_counter_account_t *counter = (tn_counter_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (counter == NULL) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_DATA_ACCESS_FAILED);
    }

    counter->counter_value = 0UL;
    tsys_emit_event((uchar const *)&counter->counter_value, sizeof(ulong));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_read(ushort account_idx) {
    tn_counter_account_t const *counter = (tn_counter_account_t const *)tsdk_get_account_data_ptr(account_idx);
    if (counter == NULL) {
        tsdk_revert(TN_COUNTER_ERR_ACCOUNT_DATA_ACCESS_FAILED);
    }

    /* Emit current value as event (read-only, no writable needed) */
    tsys_emit_event((uchar const *)&counter->counter_value, sizeof(ulong));
    tsdk_return(TSDK_SUCCESS);
}

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *instruction_data = tsdk_txn_get_instr_data(txn);
    ulong instruction_data_sz = tsdk_txn_get_instr_data_sz(txn);

    /* Check minimum size to read instruction type */
    if (instruction_data_sz < sizeof(uint)) {
        tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_DATA_SIZE);
    }

    uint instruction_type = *(uint const *)instruction_data;

    switch (instruction_type) {
        case TN_COUNTER_INSTRUCTION_CREATE: {
            if (instruction_data_sz < sizeof(tn_counter_create_args_t)) {
                tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_counter_create_args_t const *args = (tn_counter_create_args_t const *)instruction_data;
            ulong expected_size = sizeof(tn_counter_create_args_t) + args->proof_size;
            if (instruction_data_sz != expected_size) {
                tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            handle_create_counter(instruction_data, instruction_data_sz);
            break;
        }

        case TN_COUNTER_INSTRUCTION_INCREMENT:
        case TN_COUNTER_INSTRUCTION_DECREMENT:
        case TN_COUNTER_INSTRUCTION_RESET:
        case TN_COUNTER_INSTRUCTION_READ: {
            if (instruction_data_sz != sizeof(tn_counter_simple_args_t)) {
                tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_counter_simple_args_t const *args = (tn_counter_simple_args_t const *)instruction_data;
            ushort account_idx = args->account_index;

            switch (instruction_type) {
                case TN_COUNTER_INSTRUCTION_INCREMENT: handle_increment(account_idx); break;
                case TN_COUNTER_INSTRUCTION_DECREMENT: handle_decrement(account_idx); break;
                case TN_COUNTER_INSTRUCTION_RESET:     handle_reset(account_idx);     break;
                case TN_COUNTER_INSTRUCTION_READ:      handle_read(account_idx);      break;
            }
            break;
        }

        default:
            tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_TYPE);
    }

    tsdk_revert(TN_COUNTER_ERR_INVALID_INSTRUCTION_TYPE);
}

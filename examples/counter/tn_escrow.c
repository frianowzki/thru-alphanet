#include <stddef.h>
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>
#include "tn_escrow.h"

static void handle_create(uchar const *instruction_data, ulong instruction_data_sz TSDK_PARAM_UNUSED) {
    tn_escrow_create_args_t const *args = (tn_escrow_create_args_t const *)instruction_data;
    ushort account_idx = args->account_index;

    uchar const *proof_data = NULL;
    if (args->proof_size > 0) {
        proof_data = instruction_data + sizeof(tn_escrow_create_args_t);
    }

    ulong result = tsys_account_create(account_idx, args->escrow_seed, proof_data, args->proof_size);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_CREATE_FAILED);

    result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    result = tsys_account_resize(account_idx, sizeof(tn_escrow_account_t));
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_RESIZE_FAILED);

    tn_escrow_account_t *escrow = (tn_escrow_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (escrow == NULL) tsdk_revert(TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    escrow->state = TN_ESC_STATE_CREATED;
    for (ulong i = 0; i < 7; i++) escrow->padding[i] = 0;
    escrow->amount = args->amount;
    escrow->created_at = 0; /* Could use tsdk_get_current_block_ctx()->slot */
    memcpy(escrow->buyer, args->buyer, 32);
    memcpy(escrow->seller, args->seller, 32);

    /* Emit create event: amount(8) */
    tsys_emit_event((uchar const *)&escrow->amount, sizeof(ulong));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_release(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    tn_escrow_account_t *escrow = (tn_escrow_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (escrow == NULL) tsdk_revert(TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    if (escrow->state != TN_ESC_STATE_CREATED && escrow->state != TN_ESC_STATE_DISPUTED) {
        tsdk_revert(TN_ESC_ERR_INVALID_STATE);
    }

    escrow->state = TN_ESC_STATE_RELEASED;

    /* Emit release event: amount(8) + seller(32) */
    uchar event_data[40];
    memcpy(event_data, &escrow->amount, sizeof(ulong));
    memcpy(event_data + 8, escrow->seller, 32);
    tsys_emit_event(event_data, sizeof(event_data));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_dispute(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    tn_escrow_account_t *escrow = (tn_escrow_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (escrow == NULL) tsdk_revert(TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    if (escrow->state != TN_ESC_STATE_CREATED) {
        tsdk_revert(TN_ESC_ERR_INVALID_STATE);
    }

    escrow->state = TN_ESC_STATE_DISPUTED;
    tsdk_return(TSDK_SUCCESS);
}

static void handle_refund(ushort account_idx) {
    ulong result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_ESC_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    tn_escrow_account_t *escrow = (tn_escrow_account_t *)tsdk_get_account_data_ptr(account_idx);
    if (escrow == NULL) tsdk_revert(TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    if (escrow->state != TN_ESC_STATE_CREATED && escrow->state != TN_ESC_STATE_DISPUTED) {
        tsdk_revert(TN_ESC_ERR_INVALID_STATE);
    }

    escrow->state = TN_ESC_STATE_REFUNDED;

    /* Emit refund event: amount(8) + buyer(32) */
    uchar event_data[40];
    memcpy(event_data, &escrow->amount, sizeof(ulong));
    memcpy(event_data + 8, escrow->buyer, 32);
    tsys_emit_event(event_data, sizeof(event_data));
    tsdk_return(TSDK_SUCCESS);
}

static void handle_read(ushort account_idx) {
    tn_escrow_account_t const *escrow = (tn_escrow_account_t const *)tsdk_get_account_data_ptr(account_idx);
    if (escrow == NULL) tsdk_revert(TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    /* Emit state(1) + amount(8) */
    uchar event_data[9];
    event_data[0] = escrow->state;
    memcpy(event_data + 1, &escrow->amount, sizeof(ulong));
    tsys_emit_event(event_data, sizeof(event_data));
    tsdk_return(TSDK_SUCCESS);
}

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *instruction_data = tsdk_txn_get_instr_data(txn);
    ulong instruction_data_sz = tsdk_txn_get_instr_data_sz(txn);

    if (instruction_data_sz < sizeof(uint)) {
        tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_DATA_SIZE);
    }

    uint instruction_type = *(uint const *)instruction_data;

    switch (instruction_type) {
        case TN_ESC_INSTRUCTION_CREATE: {
            if (instruction_data_sz < sizeof(tn_escrow_create_args_t)) {
                tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_escrow_create_args_t const *args = (tn_escrow_create_args_t const *)instruction_data;
            ulong expected = sizeof(tn_escrow_create_args_t) + args->proof_size;
            if (instruction_data_sz != expected) {
                tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            handle_create(instruction_data, instruction_data_sz);
            break;
        }

        case TN_ESC_INSTRUCTION_RELEASE:
        case TN_ESC_INSTRUCTION_DISPUTE:
        case TN_ESC_INSTRUCTION_REFUND:
        case TN_ESC_INSTRUCTION_READ: {
            if (instruction_data_sz != sizeof(tn_escrow_simple_args_t)) {
                tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_escrow_simple_args_t const *args = (tn_escrow_simple_args_t const *)instruction_data;
            ushort account_idx = args->account_index;

            switch (instruction_type) {
                case TN_ESC_INSTRUCTION_RELEASE: handle_release(account_idx); break;
                case TN_ESC_INSTRUCTION_DISPUTE: handle_dispute(account_idx); break;
                case TN_ESC_INSTRUCTION_REFUND:  handle_refund(account_idx);  break;
                case TN_ESC_INSTRUCTION_READ:    handle_read(account_idx);    break;
            }
            break;
        }

        default:
            tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_TYPE);
    }

    tsdk_revert(TN_ESC_ERR_INVALID_INSTRUCTION_TYPE);
}

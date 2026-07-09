#include <stddef.h>
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>
#include "tn_voting.h"

static void handle_create_proposal(uchar const *instruction_data, ulong instruction_data_sz TSDK_PARAM_UNUSED) {
    tn_vote_create_args_t const *args = (tn_vote_create_args_t const *)instruction_data;
    ushort account_idx = args->account_index;

    if (args->num_options < 1 || args->num_options > TN_VOTE_MAX_OPTIONS) {
        tsdk_revert(TN_VOTE_ERR_INVALID_OPTION);
    }

    uchar const *proof_data = NULL;
    if (args->proof_size > 0) {
        proof_data = instruction_data + sizeof(tn_vote_create_args_t);
    }

    ulong result = tsys_account_create(account_idx, args->proposal_seed, proof_data, args->proof_size);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_VOTE_ERR_ACCOUNT_CREATE_FAILED);

    result = tsys_set_account_data_writable(account_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_VOTE_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    result = tsys_account_resize(account_idx, sizeof(tn_vote_proposal_t));
    if (result != TSDK_SUCCESS) tsdk_revert(TN_VOTE_ERR_ACCOUNT_RESIZE_FAILED);

    tn_vote_proposal_t *proposal = (tn_vote_proposal_t *)tsdk_get_account_data_ptr(account_idx);
    if (proposal == NULL) tsdk_revert(TN_VOTE_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    proposal->num_options = args->num_options;
    proposal->voter_limit = args->voter_limit;
    proposal->is_closed = 0;
    proposal->padding = 0;

    for (uchar i = 0; i < TN_VOTE_MAX_OPTIONS; i++) proposal->option_votes[i] = 0;
    for (ulong i = 0; i < sizeof(proposal->voted_bitmap); i++) proposal->voted_bitmap[i] = 0;

    tsdk_return(TSDK_SUCCESS);
}

static void handle_cast_vote(tn_vote_cast_args_t const *args) {
    ushort proposal_idx = args->account_index;

    ulong result = tsys_set_account_data_writable(proposal_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_VOTE_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    tn_vote_proposal_t *proposal = (tn_vote_proposal_t *)tsdk_get_account_data_ptr(proposal_idx);
    if (proposal == NULL) tsdk_revert(TN_VOTE_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    if (proposal->is_closed) tsdk_revert(TN_VOTE_ERR_PROPOSAL_CLOSED);
    if (args->option_index >= proposal->num_options) tsdk_revert(TN_VOTE_ERR_INVALID_OPTION);

    /* Check voter limit */
    if (proposal->voter_limit > 0) {
        uint total_votes = 0;
        for (uchar i = 0; i < proposal->num_options; i++) {
            total_votes += proposal->option_votes[i];
        }
        if (total_votes >= proposal->voter_limit) tsdk_revert(TN_VOTE_ERR_PROPOSAL_CLOSED);
    }

    /* Check if voter already voted using voter_id */
    uint voter_id = args->voter_id;
    if (voter_id >= TN_VOTE_MAX_VOTERS) tsdk_revert(TN_VOTE_ERR_ALREADY_VOTED);

    uchar byte_idx = (uchar)(voter_id / 8);
    uchar bit_mask = (uchar)(1U << (voter_id % 8));

    if (proposal->voted_bitmap[byte_idx] & bit_mask) {
        tsdk_revert(TN_VOTE_ERR_ALREADY_VOTED);
    }

    proposal->voted_bitmap[byte_idx] |= bit_mask;
    proposal->option_votes[args->option_index]++;

    /* Emit vote event: voter_id(4) + option(1) + new_count(4) */
    uchar event_data[9];
    memcpy(event_data, &voter_id, sizeof(uint));
    event_data[4] = args->option_index;
    uint new_count = proposal->option_votes[args->option_index];
    memcpy(event_data + 5, &new_count, sizeof(uint));
    tsys_emit_event(event_data, sizeof(event_data));

    tsdk_return(TSDK_SUCCESS);
}

static void handle_close_proposal(ushort proposal_idx) {
    ulong result = tsys_set_account_data_writable(proposal_idx);
    if (result != TSDK_SUCCESS) tsdk_revert(TN_VOTE_ERR_ACCOUNT_SET_WRITABLE_FAILED);

    tn_vote_proposal_t *proposal = (tn_vote_proposal_t *)tsdk_get_account_data_ptr(proposal_idx);
    if (proposal == NULL) tsdk_revert(TN_VOTE_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    proposal->is_closed = 1;
    tsdk_return(TSDK_SUCCESS);
}

static void handle_read_results(ushort proposal_idx) {
    tn_vote_proposal_t const *proposal = (tn_vote_proposal_t const *)tsdk_get_account_data_ptr(proposal_idx);
    if (proposal == NULL) tsdk_revert(TN_VOTE_ERR_ACCOUNT_DATA_ACCESS_FAILED);

    /* Emit vote counts as individual events for simplicity */
    for (uchar i = 0; i < proposal->num_options; i++) {
        ulong vote_data = (ulong)proposal->option_votes[i];
        tsys_emit_event((uchar const *)&vote_data, sizeof(ulong));
    }
    tsdk_return(TSDK_SUCCESS);
}

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *instruction_data = tsdk_txn_get_instr_data(txn);
    ulong instruction_data_sz = tsdk_txn_get_instr_data_sz(txn);

    if (instruction_data_sz < sizeof(uint)) {
        tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
    }

    uint instruction_type = *(uint const *)instruction_data;

    switch (instruction_type) {
        case TN_VOTE_INSTRUCTION_CREATE_PROPOSAL: {
            if (instruction_data_sz < sizeof(tn_vote_create_args_t)) {
                tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_vote_create_args_t const *args = (tn_vote_create_args_t const *)instruction_data;
            ulong expected = sizeof(tn_vote_create_args_t) + args->proof_size;
            if (instruction_data_sz != expected) {
                tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            handle_create_proposal(instruction_data, instruction_data_sz);
            break;
        }

        case TN_VOTE_INSTRUCTION_CAST_VOTE: {
            if (instruction_data_sz != sizeof(tn_vote_cast_args_t)) {
                tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            handle_cast_vote((tn_vote_cast_args_t const *)instruction_data);
            break;
        }

        case TN_VOTE_INSTRUCTION_CLOSE_PROPOSAL: {
            if (instruction_data_sz != sizeof(tn_vote_close_args_t)) {
                tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_vote_close_args_t const *args = (tn_vote_close_args_t const *)instruction_data;
            handle_close_proposal(args->account_index);
            break;
        }

        case TN_VOTE_INSTRUCTION_READ_RESULTS: {
            if (instruction_data_sz != sizeof(tn_vote_read_args_t)) {
                tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE);
            }
            tn_vote_read_args_t const *args = (tn_vote_read_args_t const *)instruction_data;
            handle_read_results(args->account_index);
            break;
        }

        default:
            tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_TYPE);
    }

    tsdk_revert(TN_VOTE_ERR_INVALID_INSTRUCTION_TYPE);
}

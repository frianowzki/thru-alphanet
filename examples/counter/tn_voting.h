#ifndef TN_VOTING_H
#define TN_VOTING_H

#include <thru-sdk/c/tn_sdk.h>

/* Error codes */
#define TN_VOTE_ERR_INVALID_INSTRUCTION_DATA_SIZE (0x2000UL)
#define TN_VOTE_ERR_INVALID_INSTRUCTION_TYPE      (0x2001UL)
#define TN_VOTE_ERR_ACCOUNT_CREATE_FAILED         (0x2002UL)
#define TN_VOTE_ERR_ACCOUNT_SET_WRITABLE_FAILED   (0x2003UL)
#define TN_VOTE_ERR_ACCOUNT_RESIZE_FAILED         (0x2004UL)
#define TN_VOTE_ERR_ACCOUNT_DATA_ACCESS_FAILED    (0x2005UL)
#define TN_VOTE_ERR_ALREADY_VOTED                 (0x2006UL)
#define TN_VOTE_ERR_INVALID_OPTION                (0x2007UL)
#define TN_VOTE_ERR_PROPOSAL_CLOSED               (0x2008UL)

/* Instruction types */
#define TN_VOTE_INSTRUCTION_CREATE_PROPOSAL  (0U)
#define TN_VOTE_INSTRUCTION_CAST_VOTE        (1U)
#define TN_VOTE_INSTRUCTION_CLOSE_PROPOSAL   (2U)
#define TN_VOTE_INSTRUCTION_READ_RESULTS     (3U)

/* Constants */
#define TN_VOTE_MAX_OPTIONS 8
#define TN_VOTE_MAX_VOTERS  64

/* Create proposal instruction */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes
    uchar proposal_seed[TN_SEED_SIZE]; // 32 bytes
    uint proof_size;                 // 4 bytes
    uchar num_options;              // 1 byte (1-8)
    uchar voter_limit;              // 1 byte (0 = unlimited)
    uchar padding[2];               // 2 bytes alignment
    /* proof_data follows */
} tn_vote_create_args_t;

/* Cast vote instruction */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes (proposal account)
    uint voter_id;                   // 4 bytes (unique voter ID)
    uchar option_index;             // 1 byte (0-based)
} tn_vote_cast_args_t;

/* Close proposal instruction */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes
} tn_vote_close_args_t;

/* Read results instruction */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes
} tn_vote_read_args_t;

/* Proposal account data layout */
typedef struct __attribute__((packed)) {
    uchar num_options;              // 1 byte
    uchar voter_limit;              // 1 byte (0 = unlimited)
    uchar is_closed;                // 1 byte
    uchar padding;                  // 1 byte
    uint option_votes[TN_VOTE_MAX_OPTIONS]; // 32 bytes
    uchar voted_bitmap[(TN_VOTE_MAX_VOTERS + 7) / 8]; // 8 bytes
} tn_vote_proposal_t;              // Total: 44 bytes

#endif

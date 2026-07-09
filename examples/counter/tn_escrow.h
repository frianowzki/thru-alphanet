#ifndef TN_ESCROW_H
#define TN_ESCROW_H

#include <thru-sdk/c/tn_sdk.h>

/* Error codes */
#define TN_ESC_ERR_INVALID_INSTRUCTION_DATA_SIZE (0x3000UL)
#define TN_ESC_ERR_INVALID_INSTRUCTION_TYPE      (0x3001UL)
#define TN_ESC_ERR_ACCOUNT_CREATE_FAILED         (0x3002UL)
#define TN_ESC_ERR_ACCOUNT_SET_WRITABLE_FAILED   (0x3003UL)
#define TN_ESC_ERR_ACCOUNT_RESIZE_FAILED         (0x3004UL)
#define TN_ESC_ERR_ACCOUNT_DATA_ACCESS_FAILED    (0x3005UL)
#define TN_ESC_ERR_INVALID_STATE                 (0x3006UL)
#define TN_ESC_ERR_UNAUTHORIZED                  (0x3007UL)
#define TN_ESC_ERR_ALREADY_FINALIZED             (0x3008UL)

/* Instruction types */
#define TN_ESC_INSTRUCTION_CREATE    (0U)
#define TN_ESC_INSTRUCTION_RELEASE   (1U)
#define TN_ESC_INSTRUCTION_DISPUTE   (2U)
#define TN_ESC_INSTRUCTION_REFUND    (3U)
#define TN_ESC_INSTRUCTION_READ      (4U)

/* Escrow states */
#define TN_ESC_STATE_CREATED   (0U)
#define TN_ESC_STATE_DISPUTED  (1U)
#define TN_ESC_STATE_RELEASED  (2U)
#define TN_ESC_STATE_REFUNDED  (3U)

/* Create escrow instruction */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes
    uchar escrow_seed[TN_SEED_SIZE]; // 32 bytes
    uint proof_size;                 // 4 bytes
    ulong amount;                    // 8 bytes (amount locked)
    uchar buyer[32];                 // 32 bytes (buyer pubkey)
    uchar seller[32];                // 32 bytes (seller pubkey)
    /* proof_data follows */
} tn_escrow_create_args_t;

/* Simple instruction (release/dispute/refund/read) */
typedef struct __attribute__((packed)) {
    uint instruction_type;           // 4 bytes
    ushort account_index;            // 2 bytes
} tn_escrow_simple_args_t;

/* Escrow account data layout */
typedef struct __attribute__((packed)) {
    uchar state;                     // 1 byte
    uchar padding[7];                // 7 bytes alignment
    ulong amount;                    // 8 bytes
    ulong created_at;                // 8 bytes (slot)
    uchar buyer[32];                 // 32 bytes
    uchar seller[32];                // 32 bytes
} tn_escrow_account_t;              // Total: 88 bytes

#endif

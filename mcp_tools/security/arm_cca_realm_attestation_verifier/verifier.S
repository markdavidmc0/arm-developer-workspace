/* Arm CCA Realm Attestation SMC Executable Primitive */
.global execute_smc_realm_call
.global _execute_smc_realm_call

.text
.align 4

/*
 * C Signature: int execute_smc_realm_call(uint64_t fid, uint64_t arg0, uint64_t *out_val);
 * x0: SMC Function Identifier (FID)
 * x1: Realm Challenge Argument
 * x2: Pointer to store output token register
 */
_execute_smc_realm_call:
execute_smc_realm_call:
    /* Push frame pointer and return address */
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp
    mov     x3, x2          /* Preserve output pointer in x3 */

    /* Execute Secure Monitor Call primitive */
    smc     #0

    /* Store returned Realm token value from x0 into output pointer */
    str     x0, [x3]
    mov     x0, #0          /* Return success code 0 */

    ldp     x29, x30, [sp], #16
    ret

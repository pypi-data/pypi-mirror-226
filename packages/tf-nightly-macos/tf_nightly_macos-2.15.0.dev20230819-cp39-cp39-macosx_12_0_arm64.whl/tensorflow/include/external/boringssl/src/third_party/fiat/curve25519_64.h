/* Autogenerated: 'src/ExtractionOCaml/unsaturated_solinas' --inline --static --use-value-barrier 25519 64 '(auto)' '2^255 - 19' carry_mul carry_square carry add sub opp selectznz to_bytes from_bytes relax carry_scmul121666 */
/* curve description: 25519 */
/* machine_wordsize = 64 (from "64") */
/* requested operations: carry_mul, carry_square, carry, add, sub, opp, selectznz, to_bytes, from_bytes, relax, carry_scmul121666 */
/* n = 5 (from "(auto)") */
/* s-c = 2^255 - [(1, 19)] (from "2^255 - 19") */
/* tight_bounds_multiplier = 1 (from "") */
/*  */
/* Computed values: */
/*   carry_chain = [0, 1, 2, 3, 4, 0, 1] */
/*   eval z = z[0] + (z[1] << 51) + (z[2] << 102) + (z[3] << 153) + (z[4] << 204) */
/*   bytes_eval z = z[0] + (z[1] << 8) + (z[2] << 16) + (z[3] << 24) + (z[4] << 32) + (z[5] << 40) + (z[6] << 48) + (z[7] << 56) + (z[8] << 64) + (z[9] << 72) + (z[10] << 80) + (z[11] << 88) + (z[12] << 96) + (z[13] << 104) + (z[14] << 112) + (z[15] << 120) + (z[16] << 128) + (z[17] << 136) + (z[18] << 144) + (z[19] << 152) + (z[20] << 160) + (z[21] << 168) + (z[22] << 176) + (z[23] << 184) + (z[24] << 192) + (z[25] << 200) + (z[26] << 208) + (z[27] << 216) + (z[28] << 224) + (z[29] << 232) + (z[30] << 240) + (z[31] << 248) */
/*   balance = [0xfffffffffffda, 0xffffffffffffe, 0xffffffffffffe, 0xffffffffffffe, 0xffffffffffffe] */

#include <stdint.h>
typedef unsigned char fiat_25519_uint1;
typedef signed char fiat_25519_int1;
#if defined(__GNUC__) || defined(__clang__)
#  define FIAT_25519_FIAT_EXTENSION __extension__
#  define FIAT_25519_FIAT_INLINE __inline__
#else
#  define FIAT_25519_FIAT_EXTENSION
#  define FIAT_25519_FIAT_INLINE
#endif

FIAT_25519_FIAT_EXTENSION typedef signed __int128 fiat_25519_int128;
FIAT_25519_FIAT_EXTENSION typedef unsigned __int128 fiat_25519_uint128;

/* The type fiat_25519_loose_field_element is a field element with loose bounds. */
/* Bounds: [[0x0 ~> 0x18000000000000], [0x0 ~> 0x18000000000000], [0x0 ~> 0x18000000000000], [0x0 ~> 0x18000000000000], [0x0 ~> 0x18000000000000]] */
typedef uint64_t fiat_25519_loose_field_element[5];

/* The type fiat_25519_tight_field_element is a field element with tight bounds. */
/* Bounds: [[0x0 ~> 0x8000000000000], [0x0 ~> 0x8000000000000], [0x0 ~> 0x8000000000000], [0x0 ~> 0x8000000000000], [0x0 ~> 0x8000000000000]] */
typedef uint64_t fiat_25519_tight_field_element[5];

#if (-1 & 3) != 3
#error "This code only works on a two's complement system"
#endif

#if !defined(FIAT_25519_NO_ASM) && (defined(__GNUC__) || defined(__clang__))
static __inline__ uint64_t fiat_25519_value_barrier_u64(uint64_t a) {
  __asm__("" : "+r"(a) : /* no inputs */);
  return a;
}
#else
#  define fiat_25519_value_barrier_u64(x) (x)
#endif


/*
 * The function fiat_25519_addcarryx_u51 is an addition with carry.
 *
 * Postconditions:
 *   out1 = (arg1 + arg2 + arg3) mod 2^51
 *   out2 = ⌊(arg1 + arg2 + arg3) / 2^51⌋
 *
 * Input Bounds:
 *   arg1: [0x0 ~> 0x1]
 *   arg2: [0x0 ~> 0x7ffffffffffff]
 *   arg3: [0x0 ~> 0x7ffffffffffff]
 * Output Bounds:
 *   out1: [0x0 ~> 0x7ffffffffffff]
 *   out2: [0x0 ~> 0x1]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_addcarryx_u51(uint64_t* out1, fiat_25519_uint1* out2, fiat_25519_uint1 arg1, uint64_t arg2, uint64_t arg3) {
  uint64_t x1;
  uint64_t x2;
  fiat_25519_uint1 x3;
  x1 = ((arg1 + arg2) + arg3);
  x2 = (x1 & UINT64_C(0x7ffffffffffff));
  x3 = (fiat_25519_uint1)(x1 >> 51);
  *out1 = x2;
  *out2 = x3;
}

/*
 * The function fiat_25519_subborrowx_u51 is a subtraction with borrow.
 *
 * Postconditions:
 *   out1 = (-arg1 + arg2 + -arg3) mod 2^51
 *   out2 = -⌊(-arg1 + arg2 + -arg3) / 2^51⌋
 *
 * Input Bounds:
 *   arg1: [0x0 ~> 0x1]
 *   arg2: [0x0 ~> 0x7ffffffffffff]
 *   arg3: [0x0 ~> 0x7ffffffffffff]
 * Output Bounds:
 *   out1: [0x0 ~> 0x7ffffffffffff]
 *   out2: [0x0 ~> 0x1]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_subborrowx_u51(uint64_t* out1, fiat_25519_uint1* out2, fiat_25519_uint1 arg1, uint64_t arg2, uint64_t arg3) {
  int64_t x1;
  fiat_25519_int1 x2;
  uint64_t x3;
  x1 = ((int64_t)(arg2 - (int64_t)arg1) - (int64_t)arg3);
  x2 = (fiat_25519_int1)(x1 >> 51);
  x3 = (x1 & UINT64_C(0x7ffffffffffff));
  *out1 = x3;
  *out2 = (fiat_25519_uint1)(0x0 - x2);
}

/*
 * The function fiat_25519_cmovznz_u64 is a single-word conditional move.
 *
 * Postconditions:
 *   out1 = (if arg1 = 0 then arg2 else arg3)
 *
 * Input Bounds:
 *   arg1: [0x0 ~> 0x1]
 *   arg2: [0x0 ~> 0xffffffffffffffff]
 *   arg3: [0x0 ~> 0xffffffffffffffff]
 * Output Bounds:
 *   out1: [0x0 ~> 0xffffffffffffffff]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_cmovznz_u64(uint64_t* out1, fiat_25519_uint1 arg1, uint64_t arg2, uint64_t arg3) {
  fiat_25519_uint1 x1;
  uint64_t x2;
  uint64_t x3;
  x1 = (!(!arg1));
  x2 = ((fiat_25519_int1)(0x0 - x1) & UINT64_C(0xffffffffffffffff));
  x3 = ((fiat_25519_value_barrier_u64(x2) & arg3) | (fiat_25519_value_barrier_u64((~x2)) & arg2));
  *out1 = x3;
}

/*
 * The function fiat_25519_carry_mul multiplies two field elements and reduces the result.
 *
 * Postconditions:
 *   eval out1 mod m = (eval arg1 * eval arg2) mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_carry_mul(fiat_25519_tight_field_element out1, const fiat_25519_loose_field_element arg1, const fiat_25519_loose_field_element arg2) {
  fiat_25519_uint128 x1;
  fiat_25519_uint128 x2;
  fiat_25519_uint128 x3;
  fiat_25519_uint128 x4;
  fiat_25519_uint128 x5;
  fiat_25519_uint128 x6;
  fiat_25519_uint128 x7;
  fiat_25519_uint128 x8;
  fiat_25519_uint128 x9;
  fiat_25519_uint128 x10;
  fiat_25519_uint128 x11;
  fiat_25519_uint128 x12;
  fiat_25519_uint128 x13;
  fiat_25519_uint128 x14;
  fiat_25519_uint128 x15;
  fiat_25519_uint128 x16;
  fiat_25519_uint128 x17;
  fiat_25519_uint128 x18;
  fiat_25519_uint128 x19;
  fiat_25519_uint128 x20;
  fiat_25519_uint128 x21;
  fiat_25519_uint128 x22;
  fiat_25519_uint128 x23;
  fiat_25519_uint128 x24;
  fiat_25519_uint128 x25;
  fiat_25519_uint128 x26;
  uint64_t x27;
  uint64_t x28;
  fiat_25519_uint128 x29;
  fiat_25519_uint128 x30;
  fiat_25519_uint128 x31;
  fiat_25519_uint128 x32;
  fiat_25519_uint128 x33;
  uint64_t x34;
  uint64_t x35;
  fiat_25519_uint128 x36;
  uint64_t x37;
  uint64_t x38;
  fiat_25519_uint128 x39;
  uint64_t x40;
  uint64_t x41;
  fiat_25519_uint128 x42;
  uint64_t x43;
  uint64_t x44;
  uint64_t x45;
  uint64_t x46;
  uint64_t x47;
  uint64_t x48;
  uint64_t x49;
  fiat_25519_uint1 x50;
  uint64_t x51;
  uint64_t x52;
  x1 = ((fiat_25519_uint128)(arg1[4]) * ((arg2[4]) * UINT8_C(0x13)));
  x2 = ((fiat_25519_uint128)(arg1[4]) * ((arg2[3]) * UINT8_C(0x13)));
  x3 = ((fiat_25519_uint128)(arg1[4]) * ((arg2[2]) * UINT8_C(0x13)));
  x4 = ((fiat_25519_uint128)(arg1[4]) * ((arg2[1]) * UINT8_C(0x13)));
  x5 = ((fiat_25519_uint128)(arg1[3]) * ((arg2[4]) * UINT8_C(0x13)));
  x6 = ((fiat_25519_uint128)(arg1[3]) * ((arg2[3]) * UINT8_C(0x13)));
  x7 = ((fiat_25519_uint128)(arg1[3]) * ((arg2[2]) * UINT8_C(0x13)));
  x8 = ((fiat_25519_uint128)(arg1[2]) * ((arg2[4]) * UINT8_C(0x13)));
  x9 = ((fiat_25519_uint128)(arg1[2]) * ((arg2[3]) * UINT8_C(0x13)));
  x10 = ((fiat_25519_uint128)(arg1[1]) * ((arg2[4]) * UINT8_C(0x13)));
  x11 = ((fiat_25519_uint128)(arg1[4]) * (arg2[0]));
  x12 = ((fiat_25519_uint128)(arg1[3]) * (arg2[1]));
  x13 = ((fiat_25519_uint128)(arg1[3]) * (arg2[0]));
  x14 = ((fiat_25519_uint128)(arg1[2]) * (arg2[2]));
  x15 = ((fiat_25519_uint128)(arg1[2]) * (arg2[1]));
  x16 = ((fiat_25519_uint128)(arg1[2]) * (arg2[0]));
  x17 = ((fiat_25519_uint128)(arg1[1]) * (arg2[3]));
  x18 = ((fiat_25519_uint128)(arg1[1]) * (arg2[2]));
  x19 = ((fiat_25519_uint128)(arg1[1]) * (arg2[1]));
  x20 = ((fiat_25519_uint128)(arg1[1]) * (arg2[0]));
  x21 = ((fiat_25519_uint128)(arg1[0]) * (arg2[4]));
  x22 = ((fiat_25519_uint128)(arg1[0]) * (arg2[3]));
  x23 = ((fiat_25519_uint128)(arg1[0]) * (arg2[2]));
  x24 = ((fiat_25519_uint128)(arg1[0]) * (arg2[1]));
  x25 = ((fiat_25519_uint128)(arg1[0]) * (arg2[0]));
  x26 = (x25 + (x10 + (x9 + (x7 + x4))));
  x27 = (uint64_t)(x26 >> 51);
  x28 = (uint64_t)(x26 & UINT64_C(0x7ffffffffffff));
  x29 = (x21 + (x17 + (x14 + (x12 + x11))));
  x30 = (x22 + (x18 + (x15 + (x13 + x1))));
  x31 = (x23 + (x19 + (x16 + (x5 + x2))));
  x32 = (x24 + (x20 + (x8 + (x6 + x3))));
  x33 = (x27 + x32);
  x34 = (uint64_t)(x33 >> 51);
  x35 = (uint64_t)(x33 & UINT64_C(0x7ffffffffffff));
  x36 = (x34 + x31);
  x37 = (uint64_t)(x36 >> 51);
  x38 = (uint64_t)(x36 & UINT64_C(0x7ffffffffffff));
  x39 = (x37 + x30);
  x40 = (uint64_t)(x39 >> 51);
  x41 = (uint64_t)(x39 & UINT64_C(0x7ffffffffffff));
  x42 = (x40 + x29);
  x43 = (uint64_t)(x42 >> 51);
  x44 = (uint64_t)(x42 & UINT64_C(0x7ffffffffffff));
  x45 = (x43 * UINT8_C(0x13));
  x46 = (x28 + x45);
  x47 = (x46 >> 51);
  x48 = (x46 & UINT64_C(0x7ffffffffffff));
  x49 = (x47 + x35);
  x50 = (fiat_25519_uint1)(x49 >> 51);
  x51 = (x49 & UINT64_C(0x7ffffffffffff));
  x52 = (x50 + x38);
  out1[0] = x48;
  out1[1] = x51;
  out1[2] = x52;
  out1[3] = x41;
  out1[4] = x44;
}

/*
 * The function fiat_25519_carry_square squares a field element and reduces the result.
 *
 * Postconditions:
 *   eval out1 mod m = (eval arg1 * eval arg1) mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_carry_square(fiat_25519_tight_field_element out1, const fiat_25519_loose_field_element arg1) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  uint64_t x6;
  uint64_t x7;
  uint64_t x8;
  fiat_25519_uint128 x9;
  fiat_25519_uint128 x10;
  fiat_25519_uint128 x11;
  fiat_25519_uint128 x12;
  fiat_25519_uint128 x13;
  fiat_25519_uint128 x14;
  fiat_25519_uint128 x15;
  fiat_25519_uint128 x16;
  fiat_25519_uint128 x17;
  fiat_25519_uint128 x18;
  fiat_25519_uint128 x19;
  fiat_25519_uint128 x20;
  fiat_25519_uint128 x21;
  fiat_25519_uint128 x22;
  fiat_25519_uint128 x23;
  fiat_25519_uint128 x24;
  uint64_t x25;
  uint64_t x26;
  fiat_25519_uint128 x27;
  fiat_25519_uint128 x28;
  fiat_25519_uint128 x29;
  fiat_25519_uint128 x30;
  fiat_25519_uint128 x31;
  uint64_t x32;
  uint64_t x33;
  fiat_25519_uint128 x34;
  uint64_t x35;
  uint64_t x36;
  fiat_25519_uint128 x37;
  uint64_t x38;
  uint64_t x39;
  fiat_25519_uint128 x40;
  uint64_t x41;
  uint64_t x42;
  uint64_t x43;
  uint64_t x44;
  uint64_t x45;
  uint64_t x46;
  uint64_t x47;
  fiat_25519_uint1 x48;
  uint64_t x49;
  uint64_t x50;
  x1 = ((arg1[4]) * UINT8_C(0x13));
  x2 = (x1 * 0x2);
  x3 = ((arg1[4]) * 0x2);
  x4 = ((arg1[3]) * UINT8_C(0x13));
  x5 = (x4 * 0x2);
  x6 = ((arg1[3]) * 0x2);
  x7 = ((arg1[2]) * 0x2);
  x8 = ((arg1[1]) * 0x2);
  x9 = ((fiat_25519_uint128)(arg1[4]) * x1);
  x10 = ((fiat_25519_uint128)(arg1[3]) * x2);
  x11 = ((fiat_25519_uint128)(arg1[3]) * x4);
  x12 = ((fiat_25519_uint128)(arg1[2]) * x2);
  x13 = ((fiat_25519_uint128)(arg1[2]) * x5);
  x14 = ((fiat_25519_uint128)(arg1[2]) * (arg1[2]));
  x15 = ((fiat_25519_uint128)(arg1[1]) * x2);
  x16 = ((fiat_25519_uint128)(arg1[1]) * x6);
  x17 = ((fiat_25519_uint128)(arg1[1]) * x7);
  x18 = ((fiat_25519_uint128)(arg1[1]) * (arg1[1]));
  x19 = ((fiat_25519_uint128)(arg1[0]) * x3);
  x20 = ((fiat_25519_uint128)(arg1[0]) * x6);
  x21 = ((fiat_25519_uint128)(arg1[0]) * x7);
  x22 = ((fiat_25519_uint128)(arg1[0]) * x8);
  x23 = ((fiat_25519_uint128)(arg1[0]) * (arg1[0]));
  x24 = (x23 + (x15 + x13));
  x25 = (uint64_t)(x24 >> 51);
  x26 = (uint64_t)(x24 & UINT64_C(0x7ffffffffffff));
  x27 = (x19 + (x16 + x14));
  x28 = (x20 + (x17 + x9));
  x29 = (x21 + (x18 + x10));
  x30 = (x22 + (x12 + x11));
  x31 = (x25 + x30);
  x32 = (uint64_t)(x31 >> 51);
  x33 = (uint64_t)(x31 & UINT64_C(0x7ffffffffffff));
  x34 = (x32 + x29);
  x35 = (uint64_t)(x34 >> 51);
  x36 = (uint64_t)(x34 & UINT64_C(0x7ffffffffffff));
  x37 = (x35 + x28);
  x38 = (uint64_t)(x37 >> 51);
  x39 = (uint64_t)(x37 & UINT64_C(0x7ffffffffffff));
  x40 = (x38 + x27);
  x41 = (uint64_t)(x40 >> 51);
  x42 = (uint64_t)(x40 & UINT64_C(0x7ffffffffffff));
  x43 = (x41 * UINT8_C(0x13));
  x44 = (x26 + x43);
  x45 = (x44 >> 51);
  x46 = (x44 & UINT64_C(0x7ffffffffffff));
  x47 = (x45 + x33);
  x48 = (fiat_25519_uint1)(x47 >> 51);
  x49 = (x47 & UINT64_C(0x7ffffffffffff));
  x50 = (x48 + x36);
  out1[0] = x46;
  out1[1] = x49;
  out1[2] = x50;
  out1[3] = x39;
  out1[4] = x42;
}

/*
 * The function fiat_25519_carry reduces a field element.
 *
 * Postconditions:
 *   eval out1 mod m = eval arg1 mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_carry(fiat_25519_tight_field_element out1, const fiat_25519_loose_field_element arg1) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  uint64_t x6;
  uint64_t x7;
  uint64_t x8;
  uint64_t x9;
  uint64_t x10;
  uint64_t x11;
  uint64_t x12;
  x1 = (arg1[0]);
  x2 = ((x1 >> 51) + (arg1[1]));
  x3 = ((x2 >> 51) + (arg1[2]));
  x4 = ((x3 >> 51) + (arg1[3]));
  x5 = ((x4 >> 51) + (arg1[4]));
  x6 = ((x1 & UINT64_C(0x7ffffffffffff)) + ((x5 >> 51) * UINT8_C(0x13)));
  x7 = ((fiat_25519_uint1)(x6 >> 51) + (x2 & UINT64_C(0x7ffffffffffff)));
  x8 = (x6 & UINT64_C(0x7ffffffffffff));
  x9 = (x7 & UINT64_C(0x7ffffffffffff));
  x10 = ((fiat_25519_uint1)(x7 >> 51) + (x3 & UINT64_C(0x7ffffffffffff)));
  x11 = (x4 & UINT64_C(0x7ffffffffffff));
  x12 = (x5 & UINT64_C(0x7ffffffffffff));
  out1[0] = x8;
  out1[1] = x9;
  out1[2] = x10;
  out1[3] = x11;
  out1[4] = x12;
}

/*
 * The function fiat_25519_add adds two field elements.
 *
 * Postconditions:
 *   eval out1 mod m = (eval arg1 + eval arg2) mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_add(fiat_25519_loose_field_element out1, const fiat_25519_tight_field_element arg1, const fiat_25519_tight_field_element arg2) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  x1 = ((arg1[0]) + (arg2[0]));
  x2 = ((arg1[1]) + (arg2[1]));
  x3 = ((arg1[2]) + (arg2[2]));
  x4 = ((arg1[3]) + (arg2[3]));
  x5 = ((arg1[4]) + (arg2[4]));
  out1[0] = x1;
  out1[1] = x2;
  out1[2] = x3;
  out1[3] = x4;
  out1[4] = x5;
}

/*
 * The function fiat_25519_sub subtracts two field elements.
 *
 * Postconditions:
 *   eval out1 mod m = (eval arg1 - eval arg2) mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_sub(fiat_25519_loose_field_element out1, const fiat_25519_tight_field_element arg1, const fiat_25519_tight_field_element arg2) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  x1 = ((UINT64_C(0xfffffffffffda) + (arg1[0])) - (arg2[0]));
  x2 = ((UINT64_C(0xffffffffffffe) + (arg1[1])) - (arg2[1]));
  x3 = ((UINT64_C(0xffffffffffffe) + (arg1[2])) - (arg2[2]));
  x4 = ((UINT64_C(0xffffffffffffe) + (arg1[3])) - (arg2[3]));
  x5 = ((UINT64_C(0xffffffffffffe) + (arg1[4])) - (arg2[4]));
  out1[0] = x1;
  out1[1] = x2;
  out1[2] = x3;
  out1[3] = x4;
  out1[4] = x5;
}

/*
 * The function fiat_25519_opp negates a field element.
 *
 * Postconditions:
 *   eval out1 mod m = -eval arg1 mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_opp(fiat_25519_loose_field_element out1, const fiat_25519_tight_field_element arg1) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  x1 = (UINT64_C(0xfffffffffffda) - (arg1[0]));
  x2 = (UINT64_C(0xffffffffffffe) - (arg1[1]));
  x3 = (UINT64_C(0xffffffffffffe) - (arg1[2]));
  x4 = (UINT64_C(0xffffffffffffe) - (arg1[3]));
  x5 = (UINT64_C(0xffffffffffffe) - (arg1[4]));
  out1[0] = x1;
  out1[1] = x2;
  out1[2] = x3;
  out1[3] = x4;
  out1[4] = x5;
}

/*
 * The function fiat_25519_selectznz is a multi-limb conditional select.
 *
 * Postconditions:
 *   eval out1 = (if arg1 = 0 then eval arg2 else eval arg3)
 *
 * Input Bounds:
 *   arg1: [0x0 ~> 0x1]
 *   arg2: [[0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff]]
 *   arg3: [[0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff]]
 * Output Bounds:
 *   out1: [[0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff], [0x0 ~> 0xffffffffffffffff]]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_selectznz(uint64_t out1[5], fiat_25519_uint1 arg1, const uint64_t arg2[5], const uint64_t arg3[5]) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  fiat_25519_cmovznz_u64(&x1, arg1, (arg2[0]), (arg3[0]));
  fiat_25519_cmovznz_u64(&x2, arg1, (arg2[1]), (arg3[1]));
  fiat_25519_cmovznz_u64(&x3, arg1, (arg2[2]), (arg3[2]));
  fiat_25519_cmovznz_u64(&x4, arg1, (arg2[3]), (arg3[3]));
  fiat_25519_cmovznz_u64(&x5, arg1, (arg2[4]), (arg3[4]));
  out1[0] = x1;
  out1[1] = x2;
  out1[2] = x3;
  out1[3] = x4;
  out1[4] = x5;
}

/*
 * The function fiat_25519_to_bytes serializes a field element to bytes in little-endian order.
 *
 * Postconditions:
 *   out1 = map (λ x, ⌊((eval arg1 mod m) mod 2^(8 * (x + 1))) / 2^(8 * x)⌋) [0..31]
 *
 * Output Bounds:
 *   out1: [[0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0x7f]]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_to_bytes(uint8_t out1[32], const fiat_25519_tight_field_element arg1) {
  uint64_t x1;
  fiat_25519_uint1 x2;
  uint64_t x3;
  fiat_25519_uint1 x4;
  uint64_t x5;
  fiat_25519_uint1 x6;
  uint64_t x7;
  fiat_25519_uint1 x8;
  uint64_t x9;
  fiat_25519_uint1 x10;
  uint64_t x11;
  uint64_t x12;
  fiat_25519_uint1 x13;
  uint64_t x14;
  fiat_25519_uint1 x15;
  uint64_t x16;
  fiat_25519_uint1 x17;
  uint64_t x18;
  fiat_25519_uint1 x19;
  uint64_t x20;
  fiat_25519_uint1 x21;
  uint64_t x22;
  uint64_t x23;
  uint64_t x24;
  uint64_t x25;
  uint8_t x26;
  uint64_t x27;
  uint8_t x28;
  uint64_t x29;
  uint8_t x30;
  uint64_t x31;
  uint8_t x32;
  uint64_t x33;
  uint8_t x34;
  uint64_t x35;
  uint8_t x36;
  uint8_t x37;
  uint64_t x38;
  uint8_t x39;
  uint64_t x40;
  uint8_t x41;
  uint64_t x42;
  uint8_t x43;
  uint64_t x44;
  uint8_t x45;
  uint64_t x46;
  uint8_t x47;
  uint64_t x48;
  uint8_t x49;
  uint8_t x50;
  uint64_t x51;
  uint8_t x52;
  uint64_t x53;
  uint8_t x54;
  uint64_t x55;
  uint8_t x56;
  uint64_t x57;
  uint8_t x58;
  uint64_t x59;
  uint8_t x60;
  uint64_t x61;
  uint8_t x62;
  uint64_t x63;
  uint8_t x64;
  fiat_25519_uint1 x65;
  uint64_t x66;
  uint8_t x67;
  uint64_t x68;
  uint8_t x69;
  uint64_t x70;
  uint8_t x71;
  uint64_t x72;
  uint8_t x73;
  uint64_t x74;
  uint8_t x75;
  uint64_t x76;
  uint8_t x77;
  uint8_t x78;
  uint64_t x79;
  uint8_t x80;
  uint64_t x81;
  uint8_t x82;
  uint64_t x83;
  uint8_t x84;
  uint64_t x85;
  uint8_t x86;
  uint64_t x87;
  uint8_t x88;
  uint64_t x89;
  uint8_t x90;
  uint8_t x91;
  fiat_25519_subborrowx_u51(&x1, &x2, 0x0, (arg1[0]), UINT64_C(0x7ffffffffffed));
  fiat_25519_subborrowx_u51(&x3, &x4, x2, (arg1[1]), UINT64_C(0x7ffffffffffff));
  fiat_25519_subborrowx_u51(&x5, &x6, x4, (arg1[2]), UINT64_C(0x7ffffffffffff));
  fiat_25519_subborrowx_u51(&x7, &x8, x6, (arg1[3]), UINT64_C(0x7ffffffffffff));
  fiat_25519_subborrowx_u51(&x9, &x10, x8, (arg1[4]), UINT64_C(0x7ffffffffffff));
  fiat_25519_cmovznz_u64(&x11, x10, 0x0, UINT64_C(0xffffffffffffffff));
  fiat_25519_addcarryx_u51(&x12, &x13, 0x0, x1, (x11 & UINT64_C(0x7ffffffffffed)));
  fiat_25519_addcarryx_u51(&x14, &x15, x13, x3, (x11 & UINT64_C(0x7ffffffffffff)));
  fiat_25519_addcarryx_u51(&x16, &x17, x15, x5, (x11 & UINT64_C(0x7ffffffffffff)));
  fiat_25519_addcarryx_u51(&x18, &x19, x17, x7, (x11 & UINT64_C(0x7ffffffffffff)));
  fiat_25519_addcarryx_u51(&x20, &x21, x19, x9, (x11 & UINT64_C(0x7ffffffffffff)));
  x22 = (x20 << 4);
  x23 = (x18 * (uint64_t)0x2);
  x24 = (x16 << 6);
  x25 = (x14 << 3);
  x26 = (uint8_t)(x12 & UINT8_C(0xff));
  x27 = (x12 >> 8);
  x28 = (uint8_t)(x27 & UINT8_C(0xff));
  x29 = (x27 >> 8);
  x30 = (uint8_t)(x29 & UINT8_C(0xff));
  x31 = (x29 >> 8);
  x32 = (uint8_t)(x31 & UINT8_C(0xff));
  x33 = (x31 >> 8);
  x34 = (uint8_t)(x33 & UINT8_C(0xff));
  x35 = (x33 >> 8);
  x36 = (uint8_t)(x35 & UINT8_C(0xff));
  x37 = (uint8_t)(x35 >> 8);
  x38 = (x25 + (uint64_t)x37);
  x39 = (uint8_t)(x38 & UINT8_C(0xff));
  x40 = (x38 >> 8);
  x41 = (uint8_t)(x40 & UINT8_C(0xff));
  x42 = (x40 >> 8);
  x43 = (uint8_t)(x42 & UINT8_C(0xff));
  x44 = (x42 >> 8);
  x45 = (uint8_t)(x44 & UINT8_C(0xff));
  x46 = (x44 >> 8);
  x47 = (uint8_t)(x46 & UINT8_C(0xff));
  x48 = (x46 >> 8);
  x49 = (uint8_t)(x48 & UINT8_C(0xff));
  x50 = (uint8_t)(x48 >> 8);
  x51 = (x24 + (uint64_t)x50);
  x52 = (uint8_t)(x51 & UINT8_C(0xff));
  x53 = (x51 >> 8);
  x54 = (uint8_t)(x53 & UINT8_C(0xff));
  x55 = (x53 >> 8);
  x56 = (uint8_t)(x55 & UINT8_C(0xff));
  x57 = (x55 >> 8);
  x58 = (uint8_t)(x57 & UINT8_C(0xff));
  x59 = (x57 >> 8);
  x60 = (uint8_t)(x59 & UINT8_C(0xff));
  x61 = (x59 >> 8);
  x62 = (uint8_t)(x61 & UINT8_C(0xff));
  x63 = (x61 >> 8);
  x64 = (uint8_t)(x63 & UINT8_C(0xff));
  x65 = (fiat_25519_uint1)(x63 >> 8);
  x66 = (x23 + (uint64_t)x65);
  x67 = (uint8_t)(x66 & UINT8_C(0xff));
  x68 = (x66 >> 8);
  x69 = (uint8_t)(x68 & UINT8_C(0xff));
  x70 = (x68 >> 8);
  x71 = (uint8_t)(x70 & UINT8_C(0xff));
  x72 = (x70 >> 8);
  x73 = (uint8_t)(x72 & UINT8_C(0xff));
  x74 = (x72 >> 8);
  x75 = (uint8_t)(x74 & UINT8_C(0xff));
  x76 = (x74 >> 8);
  x77 = (uint8_t)(x76 & UINT8_C(0xff));
  x78 = (uint8_t)(x76 >> 8);
  x79 = (x22 + (uint64_t)x78);
  x80 = (uint8_t)(x79 & UINT8_C(0xff));
  x81 = (x79 >> 8);
  x82 = (uint8_t)(x81 & UINT8_C(0xff));
  x83 = (x81 >> 8);
  x84 = (uint8_t)(x83 & UINT8_C(0xff));
  x85 = (x83 >> 8);
  x86 = (uint8_t)(x85 & UINT8_C(0xff));
  x87 = (x85 >> 8);
  x88 = (uint8_t)(x87 & UINT8_C(0xff));
  x89 = (x87 >> 8);
  x90 = (uint8_t)(x89 & UINT8_C(0xff));
  x91 = (uint8_t)(x89 >> 8);
  out1[0] = x26;
  out1[1] = x28;
  out1[2] = x30;
  out1[3] = x32;
  out1[4] = x34;
  out1[5] = x36;
  out1[6] = x39;
  out1[7] = x41;
  out1[8] = x43;
  out1[9] = x45;
  out1[10] = x47;
  out1[11] = x49;
  out1[12] = x52;
  out1[13] = x54;
  out1[14] = x56;
  out1[15] = x58;
  out1[16] = x60;
  out1[17] = x62;
  out1[18] = x64;
  out1[19] = x67;
  out1[20] = x69;
  out1[21] = x71;
  out1[22] = x73;
  out1[23] = x75;
  out1[24] = x77;
  out1[25] = x80;
  out1[26] = x82;
  out1[27] = x84;
  out1[28] = x86;
  out1[29] = x88;
  out1[30] = x90;
  out1[31] = x91;
}

/*
 * The function fiat_25519_from_bytes deserializes a field element from bytes in little-endian order.
 *
 * Postconditions:
 *   eval out1 mod m = bytes_eval arg1 mod m
 *
 * Input Bounds:
 *   arg1: [[0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0xff], [0x0 ~> 0x7f]]
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_from_bytes(fiat_25519_tight_field_element out1, const uint8_t arg1[32]) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  uint64_t x6;
  uint64_t x7;
  uint64_t x8;
  uint64_t x9;
  uint64_t x10;
  uint64_t x11;
  uint64_t x12;
  uint64_t x13;
  uint64_t x14;
  uint64_t x15;
  uint64_t x16;
  uint64_t x17;
  uint64_t x18;
  uint64_t x19;
  uint64_t x20;
  uint64_t x21;
  uint64_t x22;
  uint64_t x23;
  uint64_t x24;
  uint64_t x25;
  uint64_t x26;
  uint64_t x27;
  uint64_t x28;
  uint64_t x29;
  uint64_t x30;
  uint64_t x31;
  uint8_t x32;
  uint64_t x33;
  uint64_t x34;
  uint64_t x35;
  uint64_t x36;
  uint64_t x37;
  uint64_t x38;
  uint64_t x39;
  uint8_t x40;
  uint64_t x41;
  uint64_t x42;
  uint64_t x43;
  uint64_t x44;
  uint64_t x45;
  uint64_t x46;
  uint64_t x47;
  uint8_t x48;
  uint64_t x49;
  uint64_t x50;
  uint64_t x51;
  uint64_t x52;
  uint64_t x53;
  uint64_t x54;
  uint64_t x55;
  uint64_t x56;
  uint8_t x57;
  uint64_t x58;
  uint64_t x59;
  uint64_t x60;
  uint64_t x61;
  uint64_t x62;
  uint64_t x63;
  uint64_t x64;
  uint8_t x65;
  uint64_t x66;
  uint64_t x67;
  uint64_t x68;
  uint64_t x69;
  uint64_t x70;
  uint64_t x71;
  x1 = ((uint64_t)(arg1[31]) << 44);
  x2 = ((uint64_t)(arg1[30]) << 36);
  x3 = ((uint64_t)(arg1[29]) << 28);
  x4 = ((uint64_t)(arg1[28]) << 20);
  x5 = ((uint64_t)(arg1[27]) << 12);
  x6 = ((uint64_t)(arg1[26]) << 4);
  x7 = ((uint64_t)(arg1[25]) << 47);
  x8 = ((uint64_t)(arg1[24]) << 39);
  x9 = ((uint64_t)(arg1[23]) << 31);
  x10 = ((uint64_t)(arg1[22]) << 23);
  x11 = ((uint64_t)(arg1[21]) << 15);
  x12 = ((uint64_t)(arg1[20]) << 7);
  x13 = ((uint64_t)(arg1[19]) << 50);
  x14 = ((uint64_t)(arg1[18]) << 42);
  x15 = ((uint64_t)(arg1[17]) << 34);
  x16 = ((uint64_t)(arg1[16]) << 26);
  x17 = ((uint64_t)(arg1[15]) << 18);
  x18 = ((uint64_t)(arg1[14]) << 10);
  x19 = ((uint64_t)(arg1[13]) << 2);
  x20 = ((uint64_t)(arg1[12]) << 45);
  x21 = ((uint64_t)(arg1[11]) << 37);
  x22 = ((uint64_t)(arg1[10]) << 29);
  x23 = ((uint64_t)(arg1[9]) << 21);
  x24 = ((uint64_t)(arg1[8]) << 13);
  x25 = ((uint64_t)(arg1[7]) << 5);
  x26 = ((uint64_t)(arg1[6]) << 48);
  x27 = ((uint64_t)(arg1[5]) << 40);
  x28 = ((uint64_t)(arg1[4]) << 32);
  x29 = ((uint64_t)(arg1[3]) << 24);
  x30 = ((uint64_t)(arg1[2]) << 16);
  x31 = ((uint64_t)(arg1[1]) << 8);
  x32 = (arg1[0]);
  x33 = (x31 + (uint64_t)x32);
  x34 = (x30 + x33);
  x35 = (x29 + x34);
  x36 = (x28 + x35);
  x37 = (x27 + x36);
  x38 = (x26 + x37);
  x39 = (x38 & UINT64_C(0x7ffffffffffff));
  x40 = (uint8_t)(x38 >> 51);
  x41 = (x25 + (uint64_t)x40);
  x42 = (x24 + x41);
  x43 = (x23 + x42);
  x44 = (x22 + x43);
  x45 = (x21 + x44);
  x46 = (x20 + x45);
  x47 = (x46 & UINT64_C(0x7ffffffffffff));
  x48 = (uint8_t)(x46 >> 51);
  x49 = (x19 + (uint64_t)x48);
  x50 = (x18 + x49);
  x51 = (x17 + x50);
  x52 = (x16 + x51);
  x53 = (x15 + x52);
  x54 = (x14 + x53);
  x55 = (x13 + x54);
  x56 = (x55 & UINT64_C(0x7ffffffffffff));
  x57 = (uint8_t)(x55 >> 51);
  x58 = (x12 + (uint64_t)x57);
  x59 = (x11 + x58);
  x60 = (x10 + x59);
  x61 = (x9 + x60);
  x62 = (x8 + x61);
  x63 = (x7 + x62);
  x64 = (x63 & UINT64_C(0x7ffffffffffff));
  x65 = (uint8_t)(x63 >> 51);
  x66 = (x6 + (uint64_t)x65);
  x67 = (x5 + x66);
  x68 = (x4 + x67);
  x69 = (x3 + x68);
  x70 = (x2 + x69);
  x71 = (x1 + x70);
  out1[0] = x39;
  out1[1] = x47;
  out1[2] = x56;
  out1[3] = x64;
  out1[4] = x71;
}

/*
 * The function fiat_25519_relax is the identity function converting from tight field elements to loose field elements.
 *
 * Postconditions:
 *   out1 = arg1
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_relax(fiat_25519_loose_field_element out1, const fiat_25519_tight_field_element arg1) {
  uint64_t x1;
  uint64_t x2;
  uint64_t x3;
  uint64_t x4;
  uint64_t x5;
  x1 = (arg1[0]);
  x2 = (arg1[1]);
  x3 = (arg1[2]);
  x4 = (arg1[3]);
  x5 = (arg1[4]);
  out1[0] = x1;
  out1[1] = x2;
  out1[2] = x3;
  out1[3] = x4;
  out1[4] = x5;
}

/*
 * The function fiat_25519_carry_scmul_121666 multiplies a field element by 121666 and reduces the result.
 *
 * Postconditions:
 *   eval out1 mod m = (121666 * eval arg1) mod m
 *
 */
static FIAT_25519_FIAT_INLINE void fiat_25519_carry_scmul_121666(fiat_25519_tight_field_element out1, const fiat_25519_loose_field_element arg1) {
  fiat_25519_uint128 x1;
  fiat_25519_uint128 x2;
  fiat_25519_uint128 x3;
  fiat_25519_uint128 x4;
  fiat_25519_uint128 x5;
  uint64_t x6;
  uint64_t x7;
  fiat_25519_uint128 x8;
  uint64_t x9;
  uint64_t x10;
  fiat_25519_uint128 x11;
  uint64_t x12;
  uint64_t x13;
  fiat_25519_uint128 x14;
  uint64_t x15;
  uint64_t x16;
  fiat_25519_uint128 x17;
  uint64_t x18;
  uint64_t x19;
  uint64_t x20;
  uint64_t x21;
  fiat_25519_uint1 x22;
  uint64_t x23;
  uint64_t x24;
  fiat_25519_uint1 x25;
  uint64_t x26;
  uint64_t x27;
  x1 = ((fiat_25519_uint128)UINT32_C(0x1db42) * (arg1[4]));
  x2 = ((fiat_25519_uint128)UINT32_C(0x1db42) * (arg1[3]));
  x3 = ((fiat_25519_uint128)UINT32_C(0x1db42) * (arg1[2]));
  x4 = ((fiat_25519_uint128)UINT32_C(0x1db42) * (arg1[1]));
  x5 = ((fiat_25519_uint128)UINT32_C(0x1db42) * (arg1[0]));
  x6 = (uint64_t)(x5 >> 51);
  x7 = (uint64_t)(x5 & UINT64_C(0x7ffffffffffff));
  x8 = (x6 + x4);
  x9 = (uint64_t)(x8 >> 51);
  x10 = (uint64_t)(x8 & UINT64_C(0x7ffffffffffff));
  x11 = (x9 + x3);
  x12 = (uint64_t)(x11 >> 51);
  x13 = (uint64_t)(x11 & UINT64_C(0x7ffffffffffff));
  x14 = (x12 + x2);
  x15 = (uint64_t)(x14 >> 51);
  x16 = (uint64_t)(x14 & UINT64_C(0x7ffffffffffff));
  x17 = (x15 + x1);
  x18 = (uint64_t)(x17 >> 51);
  x19 = (uint64_t)(x17 & UINT64_C(0x7ffffffffffff));
  x20 = (x18 * UINT8_C(0x13));
  x21 = (x7 + x20);
  x22 = (fiat_25519_uint1)(x21 >> 51);
  x23 = (x21 & UINT64_C(0x7ffffffffffff));
  x24 = (x22 + x10);
  x25 = (fiat_25519_uint1)(x24 >> 51);
  x26 = (x24 & UINT64_C(0x7ffffffffffff));
  x27 = (x25 + x13);
  out1[0] = x23;
  out1[1] = x26;
  out1[2] = x27;
  out1[3] = x16;
  out1[4] = x19;
}

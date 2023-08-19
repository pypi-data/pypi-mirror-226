//===- ArmSMEDialect.h - MLIR Dialect for Arm SME ---------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file declares the Target dialect for ArmSME in MLIR.
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_DIALECT_ARMSME_IR_ARMSME_H
#define MLIR_DIALECT_ARMSME_IR_ARMSME_H

#include "mlir/Bytecode/BytecodeOpInterface.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/Dialect/Vector/IR/VectorOps.h"
#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"

#include "mlir/Dialect/ArmSME/IR/ArmSMEDialect.h.inc"

#define GET_OP_CLASSES
#include "mlir/Dialect/ArmSME/IR/ArmSME.h.inc"

#endif // MLIR_DIALECT_ARMSME_IR_ARMSME_H

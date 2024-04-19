/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "TIS-TPG-Transactions-Descriptions"
 * 	found in "asn1/TIS-TPG-Transactions-Descriptions.asn"
 * 	`asn1c -fcompound-names -fincludes-quoted -no-gen-example -R`
 */

#ifndef	_TisTpgTRM_Situation_H_
#define	_TisTpgTRM_Situation_H_


#include "asn_application.h"

/* Including external dependencies */
#include "TimestampIts.h"
#include "PairingID.h"
#include "constr_SEQUENCE.h"

#ifdef __cplusplus
extern "C" {
#endif

/* TisTpgTRM-Situation */
typedef struct TisTpgTRM_Situation {
	TimestampIts_t	 estArrivalTime;
	PairingID_t	*proposedPairingID;	/* OPTIONAL */
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} TisTpgTRM_Situation_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_TisTpgTRM_Situation;
extern asn_SEQUENCE_specifics_t asn_SPC_TisTpgTRM_Situation_specs_1;
extern asn_TYPE_member_t asn_MBR_TisTpgTRM_Situation_1[2];

#ifdef __cplusplus
}
#endif

#endif	/* _TisTpgTRM_Situation_H_ */
#include "asn_internal.h"

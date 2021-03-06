/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: status.proto */

#ifndef PROTOBUF_C_status_2eproto__INCLUDED
#define PROTOBUF_C_status_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1000000
#error This file was generated by a newer version of protoc-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1002001 < PROTOBUF_C_MIN_COMPILER_VERSION
#error This file was generated by an older version of protoc-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protoc-c.
#endif

typedef struct _PortStats PortStats;
typedef struct _Status Status;

/* --- enums --- */

typedef enum _Status__Type {
    STATUS__TYPE__FAIL = 0,
    STATUS__TYPE__SUCCESS = 1,
    STATUS__TYPE__STATS = 2 PROTOBUF_C__FORCE_ENUM_TO_BE_INT_SIZE(STATUS__TYPE)
} Status__Type;

/* --- messages --- */

struct _PortStats {
    ProtobufCMessage base;
    uint64_t n;
    uint64_t n_rtt;
    char *port;
    double avg_rxmpps;
    double std_rxmpps;
    double avg_rxbps;
    double std_rxbps;
    double avg_txmpps;
    double std_txmpps;
    double avg_txbps;
    double std_txbps;
    double avg_txwire;
    double std_txwire;
    double avg_rxwire;
    double std_rxwire;
    double rtt_avg;
    double rtt_std;
    double rtt_0;
    double rtt_25;
    double rtt_50;
    double rtt_75;
    double rtt_90;
    double rtt_95;
    double rtt_99;
    double rtt_100;
    uint64_t tx_bytes;
    uint64_t tx_pkts;
    uint64_t rx_bytes;
    uint64_t rx_pkts;
};
#define PORT_STATS__INIT                                                       \
    {                                                                          \
        PROTOBUF_C_MESSAGE_INIT(&port_stats__descriptor)                       \
        , 0, 0, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
            0, 0, 0, 0, 0, 0, 0                                                \
    }

struct _Status {
    ProtobufCMessage base;
    int32_t port;
    protobuf_c_boolean has_type;
    Status__Type type;
    size_t n_stats;
    PortStats **stats;
};
#define STATUS__INIT                                 \
    {                                                \
        PROTOBUF_C_MESSAGE_INIT(&status__descriptor) \
        , 0, 0, 0, 0, NULL                           \
    }

/* PortStats methods */
void port_stats__init(PortStats *message);
size_t port_stats__get_packed_size(const PortStats *message);
size_t port_stats__pack(const PortStats *message, uint8_t *out);
size_t port_stats__pack_to_buffer(const PortStats *message,
                                  ProtobufCBuffer *buffer);
PortStats *port_stats__unpack(ProtobufCAllocator *allocator, size_t len,
                              const uint8_t *data);
void port_stats__free_unpacked(PortStats *message,
                               ProtobufCAllocator *allocator);
/* Status methods */
void status__init(Status *message);
size_t status__get_packed_size(const Status *message);
size_t status__pack(const Status *message, uint8_t *out);
size_t status__pack_to_buffer(const Status *message, ProtobufCBuffer *buffer);
Status *status__unpack(ProtobufCAllocator *allocator, size_t len,
                       const uint8_t *data);
void status__free_unpacked(Status *message, ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*PortStats_Closure)(const PortStats *message, void *closure_data);
typedef void (*Status_Closure)(const Status *message, void *closure_data);

/* --- services --- */

/* --- descriptors --- */

extern const ProtobufCMessageDescriptor port_stats__descriptor;
extern const ProtobufCMessageDescriptor status__descriptor;
extern const ProtobufCEnumDescriptor status__type__descriptor;

PROTOBUF_C__END_DECLS

#endif /* PROTOBUF_C_status_2eproto__INCLUDED */

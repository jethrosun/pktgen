/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: proto/job.proto */

#ifndef PROTOBUF_C_proto_2fjob_2eproto__INCLUDED
#define PROTOBUF_C_proto_2fjob_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1000000
# error This file was generated by a newer version of protoc-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1002001 < PROTOBUF_C_MIN_COMPILER_VERSION
# error This file was generated by an older version of protoc-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protoc-c.
#endif


typedef struct _Job Job;


/* --- enums --- */


/* --- messages --- */

struct  _Job
{
  ProtobufCMessage base;
  protobuf_c_boolean has_tx_rate;
  int32_t tx_rate;
  protobuf_c_boolean has_duration;
  int32_t duration;
  protobuf_c_boolean has_warmup;
  int32_t warmup;
  protobuf_c_boolean has_num_flows;
  int32_t num_flows;
  protobuf_c_boolean has_port_min;
  int32_t port_min;
  protobuf_c_boolean has_port_max;
  int32_t port_max;
  protobuf_c_boolean has_size_min;
  int32_t size_min;
  protobuf_c_boolean has_size_max;
  int32_t size_max;
  protobuf_c_boolean has_life_min;
  float life_min;
  protobuf_c_boolean has_life_max;
  float life_max;
  protobuf_c_boolean has_randomize;
  protobuf_c_boolean randomize;
  protobuf_c_boolean has_latency;
  protobuf_c_boolean latency;
  protobuf_c_boolean has_online;
  protobuf_c_boolean online;
  protobuf_c_boolean has_stop;
  protobuf_c_boolean stop;
  protobuf_c_boolean has_print;
  protobuf_c_boolean print;
  protobuf_c_boolean has_tcp;
  protobuf_c_boolean tcp;
};
#define JOB__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&job__descriptor) \
    , 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0 }


/* Job methods */
void   job__init
                     (Job         *message);
size_t job__get_packed_size
                     (const Job   *message);
size_t job__pack
                     (const Job   *message,
                      uint8_t             *out);
size_t job__pack_to_buffer
                     (const Job   *message,
                      ProtobufCBuffer     *buffer);
Job *
       job__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   job__free_unpacked
                     (Job *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*Job_Closure)
                 (const Job *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor job__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_proto_2fjob_2eproto__INCLUDED */
// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/tsl/protobuf/rpc_options.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto;
namespace tensorflow {
class RPCOptions;
struct RPCOptionsDefaultTypeInternal;
extern RPCOptionsDefaultTypeInternal _RPCOptions_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::RPCOptions* Arena::CreateMaybeMessage<::tensorflow::RPCOptions>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class RPCOptions final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.RPCOptions) */ {
 public:
  inline RPCOptions() : RPCOptions(nullptr) {}
  ~RPCOptions() override;
  explicit PROTOBUF_CONSTEXPR RPCOptions(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  RPCOptions(const RPCOptions& from);
  RPCOptions(RPCOptions&& from) noexcept
    : RPCOptions() {
    *this = ::std::move(from);
  }

  inline RPCOptions& operator=(const RPCOptions& from) {
    CopyFrom(from);
    return *this;
  }
  inline RPCOptions& operator=(RPCOptions&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const RPCOptions& default_instance() {
    return *internal_default_instance();
  }
  static inline const RPCOptions* internal_default_instance() {
    return reinterpret_cast<const RPCOptions*>(
               &_RPCOptions_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(RPCOptions& a, RPCOptions& b) {
    a.Swap(&b);
  }
  inline void Swap(RPCOptions* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(RPCOptions* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  RPCOptions* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<RPCOptions>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const RPCOptions& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const RPCOptions& from) {
    RPCOptions::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(RPCOptions* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.RPCOptions";
  }
  protected:
  explicit RPCOptions(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kCompressionAlgorithmFieldNumber = 2,
    kCompressionLevelFieldNumber = 3,
    kUseRpcForInprocessMasterFieldNumber = 1,
    kCacheRpcResponseFieldNumber = 4,
    kDisableSessionConnectionSharingFieldNumber = 5,
    kNumChannelsPerTargetFieldNumber = 6,
  };
  // string compression_algorithm = 2;
  void clear_compression_algorithm();
  const std::string& compression_algorithm() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_compression_algorithm(ArgT0&& arg0, ArgT... args);
  std::string* mutable_compression_algorithm();
  PROTOBUF_NODISCARD std::string* release_compression_algorithm();
  void set_allocated_compression_algorithm(std::string* compression_algorithm);
  private:
  const std::string& _internal_compression_algorithm() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_compression_algorithm(const std::string& value);
  std::string* _internal_mutable_compression_algorithm();
  public:

  // int32 compression_level = 3;
  void clear_compression_level();
  int32_t compression_level() const;
  void set_compression_level(int32_t value);
  private:
  int32_t _internal_compression_level() const;
  void _internal_set_compression_level(int32_t value);
  public:

  // bool use_rpc_for_inprocess_master = 1;
  void clear_use_rpc_for_inprocess_master();
  bool use_rpc_for_inprocess_master() const;
  void set_use_rpc_for_inprocess_master(bool value);
  private:
  bool _internal_use_rpc_for_inprocess_master() const;
  void _internal_set_use_rpc_for_inprocess_master(bool value);
  public:

  // bool cache_rpc_response = 4;
  void clear_cache_rpc_response();
  bool cache_rpc_response() const;
  void set_cache_rpc_response(bool value);
  private:
  bool _internal_cache_rpc_response() const;
  void _internal_set_cache_rpc_response(bool value);
  public:

  // bool disable_session_connection_sharing = 5;
  void clear_disable_session_connection_sharing();
  bool disable_session_connection_sharing() const;
  void set_disable_session_connection_sharing(bool value);
  private:
  bool _internal_disable_session_connection_sharing() const;
  void _internal_set_disable_session_connection_sharing(bool value);
  public:

  // int32 num_channels_per_target = 6;
  void clear_num_channels_per_target();
  int32_t num_channels_per_target() const;
  void set_num_channels_per_target(int32_t value);
  private:
  int32_t _internal_num_channels_per_target() const;
  void _internal_set_num_channels_per_target(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.RPCOptions)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr compression_algorithm_;
    int32_t compression_level_;
    bool use_rpc_for_inprocess_master_;
    bool cache_rpc_response_;
    bool disable_session_connection_sharing_;
    int32_t num_channels_per_target_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// RPCOptions

// bool use_rpc_for_inprocess_master = 1;
inline void RPCOptions::clear_use_rpc_for_inprocess_master() {
  _impl_.use_rpc_for_inprocess_master_ = false;
}
inline bool RPCOptions::_internal_use_rpc_for_inprocess_master() const {
  return _impl_.use_rpc_for_inprocess_master_;
}
inline bool RPCOptions::use_rpc_for_inprocess_master() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.use_rpc_for_inprocess_master)
  return _internal_use_rpc_for_inprocess_master();
}
inline void RPCOptions::_internal_set_use_rpc_for_inprocess_master(bool value) {
  
  _impl_.use_rpc_for_inprocess_master_ = value;
}
inline void RPCOptions::set_use_rpc_for_inprocess_master(bool value) {
  _internal_set_use_rpc_for_inprocess_master(value);
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.use_rpc_for_inprocess_master)
}

// string compression_algorithm = 2;
inline void RPCOptions::clear_compression_algorithm() {
  _impl_.compression_algorithm_.ClearToEmpty();
}
inline const std::string& RPCOptions::compression_algorithm() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.compression_algorithm)
  return _internal_compression_algorithm();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void RPCOptions::set_compression_algorithm(ArgT0&& arg0, ArgT... args) {
 
 _impl_.compression_algorithm_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.compression_algorithm)
}
inline std::string* RPCOptions::mutable_compression_algorithm() {
  std::string* _s = _internal_mutable_compression_algorithm();
  // @@protoc_insertion_point(field_mutable:tensorflow.RPCOptions.compression_algorithm)
  return _s;
}
inline const std::string& RPCOptions::_internal_compression_algorithm() const {
  return _impl_.compression_algorithm_.Get();
}
inline void RPCOptions::_internal_set_compression_algorithm(const std::string& value) {
  
  _impl_.compression_algorithm_.Set(value, GetArenaForAllocation());
}
inline std::string* RPCOptions::_internal_mutable_compression_algorithm() {
  
  return _impl_.compression_algorithm_.Mutable(GetArenaForAllocation());
}
inline std::string* RPCOptions::release_compression_algorithm() {
  // @@protoc_insertion_point(field_release:tensorflow.RPCOptions.compression_algorithm)
  return _impl_.compression_algorithm_.Release();
}
inline void RPCOptions::set_allocated_compression_algorithm(std::string* compression_algorithm) {
  if (compression_algorithm != nullptr) {
    
  } else {
    
  }
  _impl_.compression_algorithm_.SetAllocated(compression_algorithm, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.compression_algorithm_.IsDefault()) {
    _impl_.compression_algorithm_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.RPCOptions.compression_algorithm)
}

// int32 compression_level = 3;
inline void RPCOptions::clear_compression_level() {
  _impl_.compression_level_ = 0;
}
inline int32_t RPCOptions::_internal_compression_level() const {
  return _impl_.compression_level_;
}
inline int32_t RPCOptions::compression_level() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.compression_level)
  return _internal_compression_level();
}
inline void RPCOptions::_internal_set_compression_level(int32_t value) {
  
  _impl_.compression_level_ = value;
}
inline void RPCOptions::set_compression_level(int32_t value) {
  _internal_set_compression_level(value);
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.compression_level)
}

// bool cache_rpc_response = 4;
inline void RPCOptions::clear_cache_rpc_response() {
  _impl_.cache_rpc_response_ = false;
}
inline bool RPCOptions::_internal_cache_rpc_response() const {
  return _impl_.cache_rpc_response_;
}
inline bool RPCOptions::cache_rpc_response() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.cache_rpc_response)
  return _internal_cache_rpc_response();
}
inline void RPCOptions::_internal_set_cache_rpc_response(bool value) {
  
  _impl_.cache_rpc_response_ = value;
}
inline void RPCOptions::set_cache_rpc_response(bool value) {
  _internal_set_cache_rpc_response(value);
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.cache_rpc_response)
}

// bool disable_session_connection_sharing = 5;
inline void RPCOptions::clear_disable_session_connection_sharing() {
  _impl_.disable_session_connection_sharing_ = false;
}
inline bool RPCOptions::_internal_disable_session_connection_sharing() const {
  return _impl_.disable_session_connection_sharing_;
}
inline bool RPCOptions::disable_session_connection_sharing() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.disable_session_connection_sharing)
  return _internal_disable_session_connection_sharing();
}
inline void RPCOptions::_internal_set_disable_session_connection_sharing(bool value) {
  
  _impl_.disable_session_connection_sharing_ = value;
}
inline void RPCOptions::set_disable_session_connection_sharing(bool value) {
  _internal_set_disable_session_connection_sharing(value);
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.disable_session_connection_sharing)
}

// int32 num_channels_per_target = 6;
inline void RPCOptions::clear_num_channels_per_target() {
  _impl_.num_channels_per_target_ = 0;
}
inline int32_t RPCOptions::_internal_num_channels_per_target() const {
  return _impl_.num_channels_per_target_;
}
inline int32_t RPCOptions::num_channels_per_target() const {
  // @@protoc_insertion_point(field_get:tensorflow.RPCOptions.num_channels_per_target)
  return _internal_num_channels_per_target();
}
inline void RPCOptions::_internal_set_num_channels_per_target(int32_t value) {
  
  _impl_.num_channels_per_target_ = value;
}
inline void RPCOptions::set_num_channels_per_target(int32_t value) {
  _internal_set_num_channels_per_target(value);
  // @@protoc_insertion_point(field_set:tensorflow.RPCOptions.num_channels_per_target)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2ftsl_2fprotobuf_2frpc_5foptions_2eproto

namespace OHOS {
namespace AbilityRuntime {
enum class KeepAliveSetter : int32_t {
  UNSPECIFIED = -1,
  SYSTEM = 0,
  USER = 1,
};
enum class KeepAliveAppType : int32_t {
  UNSPECIFIED = 0,
  THIRD_PARTY = 1,
  SYSTEM = 2,
};
struct KeepAliveInfo : public Parcelable {
 public:
  std::string bundleName;
  int32_t userId = -1;
  KeepAliveAppType appType = KeepAliveAppType::UNSPECIFIED;
  KeepAliveSetter setter = KeepAliveSetter::UNSPECIFIED;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static KeepAliveInfo *Unmarshalling(Parcel &parcel);
};
struct KeepAliveStatus {
  int32_t code;
  KeepAliveSetter setter;
};
}  // namespace AbilityRuntime
}  // namespace OHOS
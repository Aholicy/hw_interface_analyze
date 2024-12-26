namespace OHOS {
namespace AbilityRuntime {
struct AutoStartupInfo : public Parcelable {
 public:
  std::string bundleName;
  std::string abilityName;
  std::string moduleName;
  std::string abilityTypeName;
  std::string accessTokenId;
  int32_t appCloneIndex = 0;
  int32_t userId = -1;
  int32_t retryCount = 0;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static AutoStartupInfo *Unmarshalling(Parcel &parcel);
};
struct AutoStartupStatus {
  int32_t code = -1;
  bool isAutoStartup = false;
  bool isEdmForce = false;
};
}  // namespace AbilityRuntime
}  // namespace OHOS
namespace OHOS {
namespace AbilityRuntime {
class UIExtensionAbilityConnectInfo : public Parcelable {
 public:
  UIExtensionAbilityConnectInfo() = default;
  virtual ~UIExtensionAbilityConnectInfo() = default;
  bool ReadFromParcel(Parcel &parcel);
  bool Marshalling(Parcel &parcel) const override;
  static UIExtensionAbilityConnectInfo *Unmarshalling(Parcel &parcel);
  std::string hostBundleName = "";
  int32_t uiExtensionAbilityId = 0;
};
}  // namespace AbilityRuntime
}  // namespace OHOS
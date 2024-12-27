namespace OHOS {
namespace AbilityRuntime {
class UIExtensionSessionInfo : public Parcelable {
 public:
  UIExtensionSessionInfo() = default;
  virtual ~UIExtensionSessionInfo() = default;
  bool Marshalling(Parcel &parcel) const override;
  static UIExtensionSessionInfo *Unmarshalling(Parcel &parcel);
  int32_t persistentId = 0;
  uint32_t hostWindowId = 0;
  AAFwk::UIExtensionUsage uiExtensionUsage = AAFwk::UIExtensionUsage::MODAL;
  AppExecFwk::ElementName elementName;
  AppExecFwk::ExtensionAbilityType extensionAbilityType =
      AppExecFwk::ExtensionAbilityType::UNSPECIFIED;
};
}  // namespace AbilityRuntime
}  // namespace OHOS
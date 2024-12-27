namespace OHOS {
namespace AbilityRuntime {
class UIExtensionHostInfo : public Parcelable {
 public:
  UIExtensionHostInfo() = default;
  virtual ~UIExtensionHostInfo() = default;
  bool ReadFromParcel(Parcel &parcel);
  bool Marshalling(Parcel &parcel) const override;
  static UIExtensionHostInfo *Unmarshalling(Parcel &parcel);
  AppExecFwk::ElementName elementName_;
};
}  // namespace AbilityRuntime
}  // namespace OHOS
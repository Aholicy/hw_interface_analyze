namespace OHOS {
namespace AAFwk {
struct WindowConfig : public Parcelable {
  WindowConfig() = default;
  int32_t windowType = 0;
  uint32_t windowId = 0;
  virtual bool Marshalling(Parcel &parcel) const override;
  static WindowConfig *Unmarshalling(Parcel &parcel);
};
}  // namespace AAFwk
}  // namespace OHOS
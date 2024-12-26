namespace OHOS {
namespace AppExecFwk {
struct IntentExemptionInfo : public Parcelable {
  int32_t uid_ = 0;
  int64_t duration_ = 0;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static IntentExemptionInfo *Unmarshalling(Parcel &parcel);
};
}  // namespace AppExecFwk
}  // namespace OHOS
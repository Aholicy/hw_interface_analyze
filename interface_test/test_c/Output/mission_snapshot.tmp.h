namespace OHOS {
namespace AAFwk {
struct MissionSnapshot : public Parcelable {
  AppExecFwk::ElementName topAbility;
  bool isPrivate = false;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static MissionSnapshot *Unmarshalling(Parcel &parcel);
};
}  // namespace AAFwk
}  // namespace OHOS
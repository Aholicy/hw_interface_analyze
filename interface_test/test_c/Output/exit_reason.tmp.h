namespace OHOS {
namespace AAFwk {
struct ExitReason : public Parcelable {
  ExitReason() = default;
  ExitReason(const Reason reason, const std::string &exitMsg);
  Reason reason = Reason::REASON_UNKNOWN;
  std::string exitMsg = "";
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static ExitReason *Unmarshalling(Parcel &parcel);
};
}  // namespace AAFwk
}  // namespace OHOS
namespace OHOS {
namespace Media {
class PixelMap;
}
namespace AAFwk {
class StartWindowOption final : public Parcelable {
 public:
  StartWindowOption() = default;
  ~StartWindowOption() = default;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static StartWindowOption *Unmarshalling(Parcel &parcel);
  bool hasStartWindow = false;
  std::string startWindowBackgroundColor;
  std::shared_ptr<Media::PixelMap> startWindowIcon = nullptr;
};
}  // namespace AAFwk
}  // namespace OHOS
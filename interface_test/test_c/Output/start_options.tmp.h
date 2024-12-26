namespace OHOS {
namespace AAFwk {
class ProcessOptions;
class StartWindowOption;
class StartOptions final : public Parcelable,
                           public std::enable_shared_from_this<StartOptions> {
 public:
  const int32_t DEFAULT_DISPLAY_ID{0};
  bool windowLeftUsed_ = false;
  bool windowTopUsed_ = false;
  bool windowWidthUsed_ = false;
  bool windowHeightUsed_ = false;
  std::vector<AppExecFwk::SupportWindowMode> supportWindowModes_;
  std::shared_ptr<ProcessOptions> processOptions = nullptr;
  std::shared_ptr<StartWindowOption> startWindowOption = nullptr;
  StartOptions() = default;
  ~StartOptions() = default;
  StartOptions(const StartOptions &other);
  StartOptions &operator=(const StartOptions &other);
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static StartOptions *Unmarshalling(Parcel &parcel);
  void SetWindowMode(int32_t windowMode);
  int32_t GetWindowMode() const;
  void SetDisplayID(int32_t displayId);
  int32_t GetDisplayID() const;
  void SetWithAnimation(bool withAnimation);
  bool GetWithAnimation() const;
  void SetWindowFocused(bool windowFocused);
  int32_t GetWindowFocused() const;
  void SetWindowLeft(int32_t windowLeft);
  int32_t GetWindowLeft() const;
  void SetWindowTop(int32_t windowTop);
  int32_t GetWindowTop() const;
  void SetWindowWidth(int32_t windowWidth);
  int32_t GetWindowWidth() const;
  void SetWindowHeight(int32_t windowHeight);
  int32_t GetWindowHeight() const;

 private:
  int32_t windowMode_ =
      AbilityWindowConfiguration::MULTI_WINDOW_DISPLAY_UNDEFINED;
  int32_t displayId_ = DEFAULT_DISPLAY_ID;
  bool withAnimation_ = true;
  bool windowFocused_ = true;
  int32_t windowLeft_ = 0;
  int32_t windowTop_ = 0;
  int32_t windowWidth_ = 0;
  int32_t windowHeight_ = 0;
};
}  // namespace AAFwk
}  // namespace OHOS
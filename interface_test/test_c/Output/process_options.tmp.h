namespace OHOS {
namespace AAFwk {
enum class ProcessMode {
  UNSPECIFIED = 0,
  NEW_PROCESS_ATTACH_TO_PARENT = 1,
  NEW_PROCESS_ATTACH_TO_STATUS_BAR_ITEM = 2,
  ATTACH_TO_STATUS_BAR_ITEM = 3,
  NEW_HIDDEN_PROCESS = 4,
  NO_ATTACHMENT = 99,
  END
};
enum class StartupVisibility {
  UNSPECIFIED = -1,
  STARTUP_HIDE = 0,
  STARTUP_SHOW = 1,
  END
};
class ProcessOptions final : public Parcelable {
 public:
  ProcessOptions() = default;
  ~ProcessOptions() = default;
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static ProcessOptions *Unmarshalling(Parcel &parcel);
  static ProcessMode ConvertInt32ToProcessMode(int32_t value);
  static StartupVisibility ConvertInt32ToStartupVisibility(int32_t value);
  static bool IsNewProcessMode(ProcessMode value);
  static bool IsAttachToStatusBarMode(ProcessMode value);
  static bool IsValidProcessMode(ProcessMode value);
  static bool IsNoAttachmentMode(ProcessMode value);
  static bool IsAttachToStatusBarItemMode(ProcessMode value);
  ProcessMode processMode = ProcessMode::UNSPECIFIED;
  StartupVisibility startupVisibility = StartupVisibility::UNSPECIFIED;
  std::string processName;
  bool isRestartKeepAlive = false;
};
}  // namespace AAFwk
}  // namespace OHOS
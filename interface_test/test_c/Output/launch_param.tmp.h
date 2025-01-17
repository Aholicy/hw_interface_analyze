namespace OHOS {
namespace AAFwk {
enum LaunchReason {
  LAUNCHREASON_UNKNOWN = 0,
  LAUNCHREASON_START_ABILITY,
  LAUNCHREASON_CALL,
  LAUNCHREASON_CONTINUATION,
  LAUNCHREASON_APP_RECOVERY,
  LAUNCHREASON_SHARE,
  LAUNCHREASON_START_EXTENSION,
  LAUNCHREASON_CONNECT_EXTENSION,
  LAUNCHREASON_AUTO_STARTUP,
  LAUNCHREASON_INSIGHT_INTENT,
  LAUNCHREASON_PREPARE_CONTINUATION
};
enum LastExitReason {
  LASTEXITREASON_UNKNOWN = 0,
  LASTEXITREASON_ABILITY_NOT_RESPONDING,
  LASTEXITREASON_NORMAL,
  LASTEXITREASON_CPP_CRASH,
  LASTEXITREASON_JS_ERROR,
  LASTEXITREASON_APP_FREEZE,
  LASTEXITREASON_PERFORMANCE_CONTROL,
  LASTEXITREASON_RESOURCE_CONTROL,
  LASTEXITREASON_UPGRADE
};
enum OnContinueResult {
  ONCONTINUE_AGREE = 0,
  ONCONTINUE_REJECT,
  ONCONTINUE_MISMATCH
};
struct LaunchParam : public Parcelable {
  LaunchReason launchReason = LaunchReason::LAUNCHREASON_UNKNOWN;
  std::string launchReasonMessage = "";
  LastExitReason lastExitReason = LastExitReason::LASTEXITREASON_NORMAL;
  std::string lastExitMessage = "";
  bool ReadFromParcel(Parcel &parcel);
  virtual bool Marshalling(Parcel &parcel) const override;
  static LaunchParam *Unmarshalling(Parcel &parcel);
};
}  // namespace AAFwk
}  // namespace OHOS
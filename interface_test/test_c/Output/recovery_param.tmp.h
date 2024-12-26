namespace OHOS {
namespace AppExecFwk {
enum OnSaveResult {
  ALL_AGREE = 0,
  CONTINUATION_REJECT,
  CONTINUATION_MISMATCH,
  RECOVERY_AGREE,
  RECOVERY_REJECT,
  ALL_REJECT
};
enum StateType {
  CONTINUATION = 0,
  APP_RECOVERY,
};
enum RestartFlag {
  ALWAYS_RESTART = 0,
  RESTART_WHEN_JS_CRASH = 0x0001,
  RESTART_WHEN_APP_FREEZE = 0x0002,
  NO_RESTART = 0xFFFF,
};
enum SaveOccasionFlag {
  NO_SAVE = 0,
  SAVE_WHEN_ERROR = 1,
  SAVE_WHEN_BACKGROUND = 2,
  SAVE_ALL = 0xFF,
};
enum SaveModeFlag {
  SAVE_WITH_FILE = 1,
  SAVE_WITH_SHARED_MEMORY = 2,
};
enum StateReason {
  DEVELOPER_REQUEST,
  LIFECYCLE,
  CPP_CRASH,
  JS_ERROR,
  APP_FREEZE,
};
}  // namespace AppExecFwk
}  // namespace OHOS
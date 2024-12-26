namespace OHOS {
namespace AAFwk {
class AbilityStartSetting final
    : public Parcelable,
      public std::enable_shared_from_this<AbilityStartSetting> {
 public:
  static const std::string BOUNDS_KEY;
  static const std::string WINDOW_DISPLAY_ID_KEY;
  static const std::string WINDOW_MODE_KEY;
  static const std::string DEFAULT_RECOVERY_KEY;
  static const std::string IS_START_BY_SCB_KEY;
  AbilityStartSetting(const AbilityStartSetting &other);
  AbilityStartSetting &operator=(const AbilityStartSetting &other);
  virtual ~AbilityStartSetting() = default;
  std::set<std::string> GetPropertiesKey();
  static std::shared_ptr<AbilityStartSetting> GetEmptySetting();
  bool IsEmpty();
  void AddProperty(const std::string &key, const std::string &value);
  std::string GetProperty(const std::string &key);
  bool Marshalling(Parcel &parcel) const;
  static AbilityStartSetting *Unmarshalling(Parcel &parcel);

 protected:
  AbilityStartSetting() = default;
  friend std::shared_ptr<AbilityStartSetting> AbilityStartSettingCreator();

 private:
  std::map<std::string, std::string> abilityStarKey_;
};
}  // namespace AAFwk
}  // namespace OHOS
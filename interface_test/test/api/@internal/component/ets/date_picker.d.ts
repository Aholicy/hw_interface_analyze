/*
 * Copyright (c) 2021-2023 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file
 * @kit ArkUI
 */

/**
 * Defines the struct of DatePickerResult.
 *
 * @interface DatePickerResult
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines the struct of DatePickerResult.
 *
 * @interface DatePickerResult
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines the struct of DatePickerResult.
 *
 * @interface DatePickerResult
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare interface DatePickerResult {
  /**
   * Application year
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Application year
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Application year
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  year?: number;

  /**
   * Application month
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Application month
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Application month
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  month?: number;

  /**
   * Application day
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Application day
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Application day
   *
   * @type { ?number }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  day?: number;
}

/**
 * Defines the options of DatePicker.
 *
 * @interface DatePickerOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines the options of DatePicker.
 *
 * @interface DatePickerOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines the options of DatePicker.
 *
 * @interface DatePickerOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare interface DatePickerOptions {
  /**
   * Specifies the start date of the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Specifies the start date of the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Specifies the start date of the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  start?: Date;

  /**
   * Specifies the end date for the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Specifies the end date for the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Specifies the end date for the date selector.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  end?: Date;

  /**
   * Specifies the date selector check date or time selector check time.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Specifies the date selector check date or time selector check time.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Specifies the date selector check date or time selector check time.
   *
   * @type { ?Date }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  selected?: Date;
}

/**
 * Defines the DatePicker Component.
 *
 * @interface DatePickerInterface
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines the DatePicker Component.
 *
 * @interface DatePickerInterface
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines the DatePicker Component.
 *
 * @interface DatePickerInterface
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
interface DatePickerInterface {
  /**
   * Defines the DatePicker constructor.
   *
   * @param { DatePickerOptions } options
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Defines the DatePicker constructor.
   *
   * @param { DatePickerOptions } options
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Defines the DatePicker constructor.
   *
   * @param { DatePickerOptions } options
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  (options?: DatePickerOptions): DatePickerAttribute;
}

/**
 * Defines the DatePicker attribute functions.
 *
 * @extends CommonMethod
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines the DatePicker attribute functions.
 *
 * @extends CommonMethod
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines the DatePicker attribute functions.
 *
 * @extends CommonMethod<DatePickerAttribute>
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare class DatePickerAttribute extends CommonMethod<DatePickerAttribute> {
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @param { boolean } value
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @param { boolean } value
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @param { boolean } value
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  lunar(value: boolean): DatePickerAttribute;

  /**
   * Sets the text style of disappearing items
   *
   * @param { PickerTextStyle } value - indicates the text style of disappearing items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Sets the text style of disappearing items
   *
   * @param { PickerTextStyle } value - indicates the text style of disappearing items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  disappearTextStyle(value: PickerTextStyle): DatePickerAttribute;

  /**
   * Sets the text style of normal items
   *
   * @param { PickerTextStyle } value - indicates the text style of normal items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Sets the text style of normal items
   *
   * @param { PickerTextStyle } value - indicates the text style of normal items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  textStyle(value: PickerTextStyle): DatePickerAttribute;

  /**
   * Sets the text style of selected items
   *
   * @param { PickerTextStyle } value - indicates the text style of selected items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Sets the text style of selected items
   *
   * @param { PickerTextStyle } value - indicates the text style of selected items.
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  selectedTextStyle(value: PickerTextStyle): DatePickerAttribute;

  /**
   * This event is triggered when a DatePicker date or time is selected.
   *
   * @param { function } callback
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   * @deprecated since 10
   * @useinstead datePicker/DatePickerAttribute#onDateChange
   */
  onChange(callback: (value: DatePickerResult) => void): DatePickerAttribute;
  
  /**
   * This event is triggered when a DatePicker date or time is selected.
   *
   * @param { function } callback
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * This event is triggered when a DatePicker date or time is selected.
   *
   * @param { function } callback
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  /**
   * This event is triggered when a DatePicker date or time is selected.
   *
   * @param { Callback<Date> } callback
   * @returns { DatePickerAttribute }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onDateChange(callback: Callback<Date>): DatePickerAttribute;
}

/**
 * Provide an interface for the lunar switch style of DatePickerDialog
 * 
 * @interface LunarSwitchStyle
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 14
 */
declare interface LunarSwitchStyle {
  /**
   * Define the selected color of lunar switch.
   *
   * @type { ?ResourceColor }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  selectedColor?: ResourceColor;

  /**
   * Define the unselected color of lunar switch.
   *
   * @type { ?ResourceColor }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  unselectedColor?: ResourceColor;

  /**
   * Define the stroke color of lunar switch.
   *
   * @type { ?ResourceColor }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  strokeColor?: ResourceColor;
}

/**
 * Defines the DatePickerDialogOptions for Data Picker Dialog.
 *
 * @extends DatePickerOptions
 * @interface DatePickerDialogOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines the DatePickerDialogOptions for Data Picker Dialog.
 *
 * @extends DatePickerOptions
 * @interface DatePickerDialogOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines the DatePickerDialogOptions for Data Picker Dialog.
 *
 * @extends DatePickerOptions
 * @interface DatePickerDialogOptions
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare interface DatePickerDialogOptions extends DatePickerOptions {
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Date selector: true: displays the lunar calendar. false: The lunar calendar is not displayed.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  lunar?: boolean;

  /**
   * Whether to show the switch to display the lunar.
   * 
   * @type { ?boolean } value - indicates whether to show the switch to display the lunar
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Whether to show the switch to display the lunar.
   * 
   * @type { ?boolean } value - indicates whether to show the switch to display the lunar
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  lunarSwitch?: boolean;

  /**
   * Describes the lunar switch color.
   * 
   * @type { ?LunarSwitchStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  lunarSwitchStyle?: LunarSwitchStyle;

  /**
   * Indicates whether to show the time selector.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Indicates whether to show the time selector.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  showTime?: boolean;

  /**
   * Indicates whether to display the 24-hour clock.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Indicates whether to display the 24-hour clock.
   *
   * @type { ?boolean }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  useMilitaryTime?: boolean;

  /**
   * Text style of disappearing items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Text style of disappearing items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  disappearTextStyle?: PickerTextStyle;

  /**
   * Text style of normal items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Text style of normal items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  textStyle?: PickerTextStyle;

  /**
   * Style of accept button.
   *
   * @type { ?PickerDialogButtonStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  acceptButtonStyle?: PickerDialogButtonStyle;

  /**
   * Style of cancel button.
   *
   * @type { ?PickerDialogButtonStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  cancelButtonStyle?: PickerDialogButtonStyle;

  /**
   * Text style of selected items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Text style of selected items
   *
   * @type { ?PickerTextStyle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  selectedTextStyle?: PickerTextStyle;

  /**
   * Mask Region of dialog. The size cannot exceed the main window.
   *
   * @type { ?Rectangle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Mask Region of dialog. The size cannot exceed the main window.
   *
   * @type { ?Rectangle }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  maskRect?: Rectangle;

  /**
   * Defines the dialog alignment of the screen.
   *
   * @type { ?DialogAlignment }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Defines the dialog alignment of the screen.
   *
   * @type { ?DialogAlignment }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  alignment?: DialogAlignment;

  /**
   * Defines the dialog offset.
   *
   * @type { ?Offset }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Defines the dialog offset.
   *
   * @type { ?Offset }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  offset?: Offset;

  /**
   * Called when the OK button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   * @deprecated since 10
   * @useinstead datePicker/DatePickerDialogOptions#onDateAccept
   */
  onAccept?: (value: DatePickerResult) => void;

  /**
   * Called when the Cancel button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Called when the Cancel button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Called when the Cancel button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  /**
   * Called when the Cancel button in the dialog is clicked.
   *
   * @type { ?VoidCallback }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onCancel?: VoidCallback;

  /**
   * This event is triggered when a DatePicker date or time is selected in dialog.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   * @deprecated since 10
   * @useinstead datePicker/DatePickerDialogOptions#onDateChange
   */
  onChange?: (value: DatePickerResult) => void;
  
  /**
   * Called when the OK button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Called when the OK button in the dialog is clicked.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  /**
   * Called when the OK button in the dialog is clicked.
   *
   * @type { ?Callback<Date> }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onDateAccept?: Callback<Date>;

  /**
   * This event is triggered when a DatePicker date or time is selected in dialog.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * This event is triggered when a DatePicker date or time is selected in dialog.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  /**
   * This event is triggered when a DatePicker date or time is selected in dialog.
   *
   * @type { ?Callback<Date> }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onDateChange?: Callback<Date>;

  /**
   * Defines the datePickerDialog's background color
   *
   * @type { ?ResourceColor }
   * @default Color.Transparent
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 11
   */
  /**
   * Defines the datePickerDialog's background color
   *
   * @type { ?ResourceColor }
   * @default Color.Transparent
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  backgroundColor?: ResourceColor;

  /**
   * Defines the datePickerDialog's background blur Style
   *
   * @type { ?BlurStyle }
   * @default BlurStyle.COMPONENT_ULTRA_THICK
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 11
   */
  /**
   * Defines the datePickerDialog's background blur Style
   *
   * @type { ?BlurStyle }
   * @default BlurStyle.COMPONENT_ULTRA_THICK
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  backgroundBlurStyle?: BlurStyle;

  /**
   * Callback function when the dialog appears.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  /**
   * Callback function when the dialog appears.
   *
   * @type { ?VoidCallback }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onDidAppear?: VoidCallback;

  /**
   * Callback function when the dialog disappears.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  /**
   * Callback function when the dialog disappears.
   *
   * @type { ?VoidCallback }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onDidDisappear?: VoidCallback;

  /**
   * Callback function before the dialog openAnimation starts.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  /**
   * Callback function before the dialog openAnimation starts.
   *
   * @type { ?VoidCallback }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onWillAppear?: VoidCallback;

  /**
   * Callback function before the dialog closeAnimation starts.
   *
   * @type { ?function }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  /**
   * Callback function before the dialog closeAnimation starts.
   *
   * @type { ?VoidCallback }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  onWillDisappear?: VoidCallback;

  /**
   * Defines the dialog's shadow.
   *
   * @type { ?(ShadowOptions | ShadowStyle) }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  shadow?: ShadowOptions | ShadowStyle;

  /**
   * Set time format
   *
   * @type { ?DateTimeOptions } 
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 12
   */
  dateTimeOptions?: DateTimeOptions;

  /**
   * Defines whether to respond to the hover mode.
   *
   * @type { ?boolean }
   * @default false
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  enableHoverMode?: boolean;

  /**
   * Defines the dialog's display area in hover mode.
   *
   * @type { ?HoverModeAreaType }
   * @default HoverModeAreaType.BOTTOM_SCREEN
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 14
   */
  hoverModeArea?: HoverModeAreaType;
}

/**
 * Defines DatePickerDialog which uses show method to show DatePicker dialog.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines DatePickerDialog which uses show method to show DatePicker dialog.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines DatePickerDialog which uses show method to show DatePicker dialog.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare class DatePickerDialog {
  /**
   * Invoking method display.
   *
   * @param { DatePickerDialogOptions } options
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 8
   */
  /**
   * Invoking method display.
   *
   * @param { DatePickerDialogOptions } options
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @since 10
   */
  /**
   * Invoking method display.
   *
   * @param { DatePickerDialogOptions } options
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @crossplatform
   * @atomicservice
   * @since 11
   */
  static show(options?: DatePickerDialogOptions);
}

/**
 * Defines DatePicker Component.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines DatePicker Component.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines DatePicker Component.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare const DatePicker: DatePickerInterface;

/**
 * Defines DatePicker Component instance.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 8
 */
/**
 * Defines DatePicker Component instance.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @since 10
 */
/**
 * Defines DatePicker Component instance.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 11
 */
declare const DatePickerInstance: DatePickerAttribute;



/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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
 * @file Refresh modifier file，defines modifier and function.
 * @kit ArkUI
 */




/**
 * Defines Refresh Modifier
 *
 * @extends RefreshAttribute
 * @implements AttributeModifier<RefreshAttribute>
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @atomicservice
 * @since 12
*/
export declare class RefreshModifier extends RefreshAttribute implements AttributeModifier<RefreshAttribute> {

    /**
     * Defines the normal update attribute function.
     * 
     * @param { RefreshAttribute } instance
     * @syscap SystemCapability.ArkUI.ArkUI.Full
     * @crossplatform
     * @atomicservice
     * @since 12
     */
    applyNormalAttribute?(instance: RefreshAttribute): void;
  }
  
"use strict";
(self["webpackChunkvdk_jupyterlab_extension"] = self["webpackChunkvdk_jupyterlab_extension"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_vdkDialogs_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./vdkDialogs.css */ "./node_modules/css-loader/dist/cjs.js!./style/vdkDialogs.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_vdkDialogs_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2021-2023 VMware, Inc.\n * SPDX-License-Identifier: Apache-2.0\n */\n/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n.jp-vdk-cell {\n  --jp-cell-editor-background: rgb(240 246 255);\n}\n\n.jp-vdk-cell-dark {\n  --jp-cell-editor-background: rgb(6 27 59);\n}\n\n.jp-vdk-cell-num {\n  position: absolute;\n  top: 0;\n  right: 0;\n  background-color: #1e488c;\n  color: aliceblue;\n  padding: 4px;\n}\n\n.jp-vdk-logo {\n  position: absolute;\n  top: 0;\n  right: -5px;\n  padding-right: 25px;\n}\n\n.jp-vdk-failing-cell {\n  --jp-cell-editor-border-color: #8c1e1e;\n  --jp-cell-editor-box-shadow: inset 0 0 2px #8c1e1e;\n}\n\n.jp-vdk-failing-cell-num {\n  position: absolute;\n  top: 0;\n  right: 0;\n  background-color: #8c1e1e;\n  color: aliceblue;\n  padding: 4px;\n}\n\n.jp-vdk-failing-cell-prompt {\n  --jp-cell-prompt-not-active-font-color: #8c1e1e;\n  --jp-cell-inprompt-font-color: #8c1e1e;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;EAGE;AACF;;;;CAIC;;AAGD;EACE,6CAA6C;AAC/C;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,kBAAkB;EAClB,MAAM;EACN,QAAQ;EACR,yBAAyB;EACzB,gBAAgB;EAChB,YAAY;AACd;;AAEA;EACE,kBAAkB;EAClB,MAAM;EACN,WAAW;EACX,mBAAmB;AACrB;;AAEA;EACE,sCAAsC;EACtC,kDAAkD;AACpD;;AAEA;EACE,kBAAkB;EAClB,MAAM;EACN,QAAQ;EACR,yBAAyB;EACzB,gBAAgB;EAChB,YAAY;AACd;;AAEA;EACE,+CAA+C;EAC/C,sCAAsC;AACxC","sourcesContent":["/*\n * Copyright 2021-2023 VMware, Inc.\n * SPDX-License-Identifier: Apache-2.0\n */\n/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n@import url('vdkDialogs.css');\n\n.jp-vdk-cell {\n  --jp-cell-editor-background: rgb(240 246 255);\n}\n\n.jp-vdk-cell-dark {\n  --jp-cell-editor-background: rgb(6 27 59);\n}\n\n.jp-vdk-cell-num {\n  position: absolute;\n  top: 0;\n  right: 0;\n  background-color: #1e488c;\n  color: aliceblue;\n  padding: 4px;\n}\n\n.jp-vdk-logo {\n  position: absolute;\n  top: 0;\n  right: -5px;\n  padding-right: 25px;\n}\n\n.jp-vdk-failing-cell {\n  --jp-cell-editor-border-color: #8c1e1e;\n  --jp-cell-editor-box-shadow: inset 0 0 2px #8c1e1e;\n}\n\n.jp-vdk-failing-cell-num {\n  position: absolute;\n  top: 0;\n  right: 0;\n  background-color: #8c1e1e;\n  color: aliceblue;\n  padding: 4px;\n}\n\n.jp-vdk-failing-cell-prompt {\n  --jp-cell-prompt-not-active-font-color: #8c1e1e;\n  --jp-cell-inprompt-font-color: #8c1e1e;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/vdkDialogs.css":
/*!********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/vdkDialogs.css ***!
  \********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2021-2023 VMware, Inc.\n * SPDX-License-Identifier: Apache-2.0\n */\n\n.jp-vdk-input-wrapper {\n  display: flex;\n  flex-direction: column;\n  margin-top: 15px;\n}\n\n.hidden {\n  display: none;\n}\n\n.jp-vdk-checkbox-wrappers {\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  margin-left: 0;\n  padding-left: 0;\n}\n\n.jp-vdk-checkbox {\n  margin-right: 10px;\n}\n\n#enable {\n  margin-top: 10px;\n  margin-left: 0;\n}\n\n.vdk-run-error-message {\n  color: #c0392b;\n  padding: 16px;\n  font-weight: bold;\n  display: flex;\n  align-items: center;\n}\n\n.vdk-run-error-message p {\n  padding-bottom: 10px;\n}\n\n.vdk-run-error-message a {\n  color: #11239a;\n  text-decoration: underline;\n}\n\n.vdk-run-dialog-message {\n  font-size: 16px;\n  color: #33b53a;\n}\n.vdk-run-dialog-message-container {\n  display: flex;\n  align-items: center;\n}\n\n.vdk-status-dialog-message {\n  font-size: 16px;\n  padding: 20px;\n}\n\n.jp-vdk-check-status-button {\n  position: absolute;\n  right: 1px;\n  border-radius: 5px;\n  border: none;\n}\n\n.jp-vdk-status-button-content {\n  display: flex;\n  align-items: center;\n}\n\n.jp-vdk-check-status-button .jp-vdk-logo {\n  position: static;\n  padding-right: 5px;\n}\n\n.jp-vdk-check-status-button:hover {\n  background-color: #e0e0e0;\n  cursor: pointer;\n}\n\n.vdk-dialog-check-icon {\n  margin-right: 10px;\n}\n\n.vdk-convert-to-notebook-error-message {\n  display: flex;\n  font-size: 16px;\n  color: #c0392b;\n}\n\n.vdk-dialog-error-icon .jp-icon3[fill] {\n  fill: #c0392b;\n}\n\n.vdk-dialog-check-icon .jp-icon3[fill] {\n  fill: #33b53a;\n}\n\n.vdk-error-dialog {\n  font-size: 16px;\n  color: #c0392b;\n  display: flex;\n  align-items: center;\n}\n\n.vdk-dialog-error-icon {\n  margin-right: 10px;\n  display: flex;\n  align-items: center;\n}\n\n.jp-vdk-login2-input {\n  width: 80%;\n}\n\n.jp-vdk-login2-button {\n  padding: 8px 16px;\n  border: 1px solid #ccc;\n  background: linear-gradient(to bottom, #f7f7f7, #e7e7e7);\n  font-weight: 600;\n  border-radius: 2px;\n  cursor: pointer;\n  color: #333;\n  text-align: center;\n  font-size: 14px;\n  transition: background 0.3s;\n}\n\n.jp-vdk-login2-button:hover {\n  background: linear-gradient(to bottom, #e7e7e7, #d7d7d7);\n}\n\n.jp-vdk-login2-dialog-container {\n  text-align: left;\n  padding: 20px;\n  width: 600px;\n}\n", "",{"version":3,"sources":["webpack://./style/vdkDialogs.css"],"names":[],"mappings":"AAAA;;;EAGE;;AAEF;EACE,aAAa;EACb,sBAAsB;EACtB,gBAAgB;AAClB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,aAAa;EACb,2BAA2B;EAC3B,mBAAmB;EACnB,cAAc;EACd,eAAe;AACjB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,gBAAgB;EAChB,cAAc;AAChB;;AAEA;EACE,cAAc;EACd,aAAa;EACb,iBAAiB;EACjB,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,oBAAoB;AACtB;;AAEA;EACE,cAAc;EACd,0BAA0B;AAC5B;;AAEA;EACE,eAAe;EACf,cAAc;AAChB;AACA;EACE,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,eAAe;EACf,aAAa;AACf;;AAEA;EACE,kBAAkB;EAClB,UAAU;EACV,kBAAkB;EAClB,YAAY;AACd;;AAEA;EACE,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,gBAAgB;EAChB,kBAAkB;AACpB;;AAEA;EACE,yBAAyB;EACzB,eAAe;AACjB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,aAAa;EACb,eAAe;EACf,cAAc;AAChB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,eAAe;EACf,cAAc;EACd,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,kBAAkB;EAClB,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,UAAU;AACZ;;AAEA;EACE,iBAAiB;EACjB,sBAAsB;EACtB,wDAAwD;EACxD,gBAAgB;EAChB,kBAAkB;EAClB,eAAe;EACf,WAAW;EACX,kBAAkB;EAClB,eAAe;EACf,2BAA2B;AAC7B;;AAEA;EACE,wDAAwD;AAC1D;;AAEA;EACE,gBAAgB;EAChB,aAAa;EACb,YAAY;AACd","sourcesContent":["/*\n * Copyright 2021-2023 VMware, Inc.\n * SPDX-License-Identifier: Apache-2.0\n */\n\n.jp-vdk-input-wrapper {\n  display: flex;\n  flex-direction: column;\n  margin-top: 15px;\n}\n\n.hidden {\n  display: none;\n}\n\n.jp-vdk-checkbox-wrappers {\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  margin-left: 0;\n  padding-left: 0;\n}\n\n.jp-vdk-checkbox {\n  margin-right: 10px;\n}\n\n#enable {\n  margin-top: 10px;\n  margin-left: 0;\n}\n\n.vdk-run-error-message {\n  color: #c0392b;\n  padding: 16px;\n  font-weight: bold;\n  display: flex;\n  align-items: center;\n}\n\n.vdk-run-error-message p {\n  padding-bottom: 10px;\n}\n\n.vdk-run-error-message a {\n  color: #11239a;\n  text-decoration: underline;\n}\n\n.vdk-run-dialog-message {\n  font-size: 16px;\n  color: #33b53a;\n}\n.vdk-run-dialog-message-container {\n  display: flex;\n  align-items: center;\n}\n\n.vdk-status-dialog-message {\n  font-size: 16px;\n  padding: 20px;\n}\n\n.jp-vdk-check-status-button {\n  position: absolute;\n  right: 1px;\n  border-radius: 5px;\n  border: none;\n}\n\n.jp-vdk-status-button-content {\n  display: flex;\n  align-items: center;\n}\n\n.jp-vdk-check-status-button .jp-vdk-logo {\n  position: static;\n  padding-right: 5px;\n}\n\n.jp-vdk-check-status-button:hover {\n  background-color: #e0e0e0;\n  cursor: pointer;\n}\n\n.vdk-dialog-check-icon {\n  margin-right: 10px;\n}\n\n.vdk-convert-to-notebook-error-message {\n  display: flex;\n  font-size: 16px;\n  color: #c0392b;\n}\n\n.vdk-dialog-error-icon .jp-icon3[fill] {\n  fill: #c0392b;\n}\n\n.vdk-dialog-check-icon .jp-icon3[fill] {\n  fill: #33b53a;\n}\n\n.vdk-error-dialog {\n  font-size: 16px;\n  color: #c0392b;\n  display: flex;\n  align-items: center;\n}\n\n.vdk-dialog-error-icon {\n  margin-right: 10px;\n  display: flex;\n  align-items: center;\n}\n\n.jp-vdk-login2-input {\n  width: 80%;\n}\n\n.jp-vdk-login2-button {\n  padding: 8px 16px;\n  border: 1px solid #ccc;\n  background: linear-gradient(to bottom, #f7f7f7, #e7e7e7);\n  font-weight: 600;\n  border-radius: 2px;\n  cursor: pointer;\n  color: #333;\n  text-align: center;\n  font-size: 14px;\n  transition: background 0.3s;\n}\n\n.jp-vdk-login2-button:hover {\n  background: linear-gradient(to bottom, #e7e7e7, #d7d7d7);\n}\n\n.jp-vdk-login2-dialog-container {\n  text-align: left;\n  padding: 20px;\n  width: 600px;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");
/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */




/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ })

}]);
//# sourceMappingURL=style_index_js.647b942c51041e068d0f.js.map
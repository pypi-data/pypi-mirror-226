"use strict";
(self["webpackChunkvoila_topbar"] = self["webpackChunkvoila_topbar"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);






/**
 * Initialization data for the voila_topbar extension.
 */
const plugin = {
    id: 'voila_topbar:plugin',
    description: 'A Voila extension',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.IJupyterWidgetRegistry],
    activate: (app, themeManager) => {
        var _a;
        if (app.name !== 'Voila') {
            return;
        }
        const kernelConnection = (_a = app === null || app === void 0 ? void 0 : app.widgetManager) === null || _a === void 0 ? void 0 : _a.kernel;
        const extensionConfig = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getOption('extensionConfig'));
        const config = extensionConfig['voila_topbar'];
        const widget = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3__.createElement(_widget__WEBPACK_IMPORTED_MODULE_5__.TopbarElement, { config: config, themeManager: themeManager, kernelConnection: kernelConnection }));
        widget.id = 'voila-topbar-element';
        app.shell.add(widget, 'top');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/kernelStatus.js":
/*!*****************************!*\
  !*** ./lib/kernelStatus.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ProgressCircle: () => (/* binding */ ProgressCircle)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

function ProgressCircle(props) {
    const radius = 104;
    const d = (progress) => {
        const angle = Math.max(progress * 3.6, 0.1);
        const rad = (angle * Math.PI) / 180, x = Math.sin(rad) * radius, y = Math.cos(rad) * -radius, mid = angle < 180 ? 1 : 0, shape = `M 0 0 v -${radius} A ${radius} ${radius} 1 ` +
            mid +
            ' 0 ' +
            x.toFixed(4) +
            ' ' +
            y.toFixed(4) +
            ' z';
        return shape;
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'jp-Statusbar-ProgressCircle', role: "progressbar", "aria-label": props.label || 'Unlabelled progress circle', "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": props.progress, style: { margin: 'auto' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { viewBox: "0 0 250 250" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("circle", { cx: "125", cy: "125", r: `${radius}`, strokeWidth: "20", fill: "none" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { transform: "translate(125,125) scale(.9)", d: d(props.progress), fill: '#f0f8ff' }))));
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TopbarElement: () => (/* binding */ TopbarElement)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _kernelStatus__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./kernelStatus */ "./lib/kernelStatus.js");


function TopbarElement(props) {
    const config = react__WEBPACK_IMPORTED_MODULE_0__.useMemo(() => {
        if (props.config) {
            return props.config;
        }
        return {
            background: 'red',
            title: 'Voila Dashboard',
            themeToggle: true,
            kernelActivity: true
        };
    }, [props.config]);
    const [themeOptions, setThemeOptions] = react__WEBPACK_IMPORTED_MODULE_0__.useState([
        ...props.themeManager.themes
    ]);
    const [kernelBusy, setkernelBusy] = react__WEBPACK_IMPORTED_MODULE_0__.useState(100);
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        const cb = (sender, args) => {
            if (args.newValue.length > 0) {
                return;
            }
            setThemeOptions([...props.themeManager.themes]);
        };
        props.themeManager.themeChanged.connect(cb);
        const kernelCb = (sender, status) => {
            const progress = status === 'busy' ? 0 : 100;
            setkernelBusy(progress);
        };
        if (props.kernelConnection) {
            props.kernelConnection.statusChanged.connect(kernelCb);
        }
        return () => {
            props.themeManager.themeChanged.disconnect(cb);
            if (props.kernelConnection) {
                props.kernelConnection.statusChanged.disconnect(kernelCb);
            }
        };
    }, [props.themeManager, props.kernelConnection]);
    const onThemeChange = react__WEBPACK_IMPORTED_MODULE_0__.useCallback((e) => {
        var _a;
        const theme = (_a = e.currentTarget) === null || _a === void 0 ? void 0 : _a.value;
        if (theme) {
            props.themeManager.setTheme(theme);
        }
    }, [props.themeManager]);
    const themeSelect = react__WEBPACK_IMPORTED_MODULE_0__.useMemo(() => {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("select", { className: "voila-topbar-theme", onChange: onThemeChange }, themeOptions.map(el => {
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { key: el, value: el, style: { background: 'var(--jp-layout-color2)' } }, el));
        })));
    }, [themeOptions, onThemeChange]);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "voila-topbar" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "voila-topbar-title" }, config.title),
        themeSelect,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_kernelStatus__WEBPACK_IMPORTED_MODULE_1__.ProgressCircle, { progress: kernelBusy, width: 50, height: 50 })));
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.43dea8e6c75dfad37ace.js.map
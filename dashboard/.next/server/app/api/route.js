/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "app/api/route";
exports.ids = ["app/api/route"];
exports.modules = {

/***/ "next/dist/compiled/next-server/app-page.runtime.dev.js":
/*!*************************************************************************!*\
  !*** external "next/dist/compiled/next-server/app-page.runtime.dev.js" ***!
  \*************************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/compiled/next-server/app-page.runtime.dev.js");

/***/ }),

/***/ "next/dist/compiled/next-server/app-route.runtime.dev.js":
/*!**************************************************************************!*\
  !*** external "next/dist/compiled/next-server/app-route.runtime.dev.js" ***!
  \**************************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/compiled/next-server/app-route.runtime.dev.js");

/***/ }),

/***/ "../app-render/work-async-storage.external":
/*!*****************************************************************************!*\
  !*** external "next/dist/server/app-render/work-async-storage.external.js" ***!
  \*****************************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/server/app-render/work-async-storage.external.js");

/***/ }),

/***/ "./work-unit-async-storage.external":
/*!**********************************************************************************!*\
  !*** external "next/dist/server/app-render/work-unit-async-storage.external.js" ***!
  \**********************************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/server/app-render/work-unit-async-storage.external.js");

/***/ }),

/***/ "buffer":
/*!*************************!*\
  !*** external "buffer" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("buffer");

/***/ }),

/***/ "crypto":
/*!*************************!*\
  !*** external "crypto" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("crypto");

/***/ }),

/***/ "stream":
/*!*************************!*\
  !*** external "stream" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("stream");

/***/ }),

/***/ "util":
/*!***********************!*\
  !*** external "util" ***!
  \***********************/
/***/ ((module) => {

"use strict";
module.exports = require("util");

/***/ }),

/***/ "(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader/index.js?name=app%2Fapi%2Froute&page=%2Fapi%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Froute.js&appDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard%5Capp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/next/dist/build/webpack/loaders/next-app-loader/index.js?name=app%2Fapi%2Froute&page=%2Fapi%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Froute.js&appDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard%5Capp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D! ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   patchFetch: () => (/* binding */ patchFetch),\n/* harmony export */   routeModule: () => (/* binding */ routeModule),\n/* harmony export */   serverHooks: () => (/* binding */ serverHooks),\n/* harmony export */   workAsyncStorage: () => (/* binding */ workAsyncStorage),\n/* harmony export */   workUnitAsyncStorage: () => (/* binding */ workUnitAsyncStorage)\n/* harmony export */ });\n/* harmony import */ var next_dist_server_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! next/dist/server/route-modules/app-route/module.compiled */ \"(rsc)/./node_modules/next/dist/server/route-modules/app-route/module.compiled.js\");\n/* harmony import */ var next_dist_server_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(next_dist_server_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var next_dist_server_route_kind__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! next/dist/server/route-kind */ \"(rsc)/./node_modules/next/dist/server/route-kind.js\");\n/* harmony import */ var next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! next/dist/server/lib/patch-fetch */ \"(rsc)/./node_modules/next/dist/server/lib/patch-fetch.js\");\n/* harmony import */ var next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var C_Users_patrisio_Desktop_Carnavacs_dashboard_app_api_route_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app/api/route.js */ \"(rsc)/./app/api/route.js\");\n\n\n\n\n// We inject the nextConfigOutput here so that we can use them in the route\n// module.\nconst nextConfigOutput = \"\"\nconst routeModule = new next_dist_server_route_modules_app_route_module_compiled__WEBPACK_IMPORTED_MODULE_0__.AppRouteRouteModule({\n    definition: {\n        kind: next_dist_server_route_kind__WEBPACK_IMPORTED_MODULE_1__.RouteKind.APP_ROUTE,\n        page: \"/api/route\",\n        pathname: \"/api\",\n        filename: \"route\",\n        bundlePath: \"app/api/route\"\n    },\n    resolvedPagePath: \"C:\\\\Users\\\\patrisio\\\\Desktop\\\\Carnavacs\\\\dashboard\\\\app\\\\api\\\\route.js\",\n    nextConfigOutput,\n    userland: C_Users_patrisio_Desktop_Carnavacs_dashboard_app_api_route_js__WEBPACK_IMPORTED_MODULE_3__\n});\n// Pull out the exports that we need to expose from the module. This should\n// be eliminated when we've moved the other routes to the new format. These\n// are used to hook into the route.\nconst { workAsyncStorage, workUnitAsyncStorage, serverHooks } = routeModule;\nfunction patchFetch() {\n    return (0,next_dist_server_lib_patch_fetch__WEBPACK_IMPORTED_MODULE_2__.patchFetch)({\n        workAsyncStorage,\n        workUnitAsyncStorage\n    });\n}\n\n\n//# sourceMappingURL=app-route.js.map//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvbmV4dC9kaXN0L2J1aWxkL3dlYnBhY2svbG9hZGVycy9uZXh0LWFwcC1sb2FkZXIvaW5kZXguanM/bmFtZT1hcHAlMkZhcGklMkZyb3V0ZSZwYWdlPSUyRmFwaSUyRnJvdXRlJmFwcFBhdGhzPSZwYWdlUGF0aD1wcml2YXRlLW5leHQtYXBwLWRpciUyRmFwaSUyRnJvdXRlLmpzJmFwcERpcj1DJTNBJTVDVXNlcnMlNUNwYXRyaXNpbyU1Q0Rlc2t0b3AlNUNDYXJuYXZhY3MlNUNkYXNoYm9hcmQlNUNhcHAmcGFnZUV4dGVuc2lvbnM9dHN4JnBhZ2VFeHRlbnNpb25zPXRzJnBhZ2VFeHRlbnNpb25zPWpzeCZwYWdlRXh0ZW5zaW9ucz1qcyZyb290RGlyPUMlM0ElNUNVc2VycyU1Q3BhdHJpc2lvJTVDRGVza3RvcCU1Q0Nhcm5hdmFjcyU1Q2Rhc2hib2FyZCZpc0Rldj10cnVlJnRzY29uZmlnUGF0aD10c2NvbmZpZy5qc29uJmJhc2VQYXRoPSZhc3NldFByZWZpeD0mbmV4dENvbmZpZ091dHB1dD0mcHJlZmVycmVkUmVnaW9uPSZtaWRkbGV3YXJlQ29uZmlnPWUzMCUzRCEiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7QUFBK0Y7QUFDdkM7QUFDcUI7QUFDc0I7QUFDbkc7QUFDQTtBQUNBO0FBQ0Esd0JBQXdCLHlHQUFtQjtBQUMzQztBQUNBLGNBQWMsa0VBQVM7QUFDdkI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLFlBQVk7QUFDWixDQUFDO0FBQ0Q7QUFDQTtBQUNBO0FBQ0EsUUFBUSxzREFBc0Q7QUFDOUQ7QUFDQSxXQUFXLDRFQUFXO0FBQ3RCO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDMEY7O0FBRTFGIiwic291cmNlcyI6WyIiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgQXBwUm91dGVSb3V0ZU1vZHVsZSB9IGZyb20gXCJuZXh0L2Rpc3Qvc2VydmVyL3JvdXRlLW1vZHVsZXMvYXBwLXJvdXRlL21vZHVsZS5jb21waWxlZFwiO1xuaW1wb3J0IHsgUm91dGVLaW5kIH0gZnJvbSBcIm5leHQvZGlzdC9zZXJ2ZXIvcm91dGUta2luZFwiO1xuaW1wb3J0IHsgcGF0Y2hGZXRjaCBhcyBfcGF0Y2hGZXRjaCB9IGZyb20gXCJuZXh0L2Rpc3Qvc2VydmVyL2xpYi9wYXRjaC1mZXRjaFwiO1xuaW1wb3J0ICogYXMgdXNlcmxhbmQgZnJvbSBcIkM6XFxcXFVzZXJzXFxcXHBhdHJpc2lvXFxcXERlc2t0b3BcXFxcQ2FybmF2YWNzXFxcXGRhc2hib2FyZFxcXFxhcHBcXFxcYXBpXFxcXHJvdXRlLmpzXCI7XG4vLyBXZSBpbmplY3QgdGhlIG5leHRDb25maWdPdXRwdXQgaGVyZSBzbyB0aGF0IHdlIGNhbiB1c2UgdGhlbSBpbiB0aGUgcm91dGVcbi8vIG1vZHVsZS5cbmNvbnN0IG5leHRDb25maWdPdXRwdXQgPSBcIlwiXG5jb25zdCByb3V0ZU1vZHVsZSA9IG5ldyBBcHBSb3V0ZVJvdXRlTW9kdWxlKHtcbiAgICBkZWZpbml0aW9uOiB7XG4gICAgICAgIGtpbmQ6IFJvdXRlS2luZC5BUFBfUk9VVEUsXG4gICAgICAgIHBhZ2U6IFwiL2FwaS9yb3V0ZVwiLFxuICAgICAgICBwYXRobmFtZTogXCIvYXBpXCIsXG4gICAgICAgIGZpbGVuYW1lOiBcInJvdXRlXCIsXG4gICAgICAgIGJ1bmRsZVBhdGg6IFwiYXBwL2FwaS9yb3V0ZVwiXG4gICAgfSxcbiAgICByZXNvbHZlZFBhZ2VQYXRoOiBcIkM6XFxcXFVzZXJzXFxcXHBhdHJpc2lvXFxcXERlc2t0b3BcXFxcQ2FybmF2YWNzXFxcXGRhc2hib2FyZFxcXFxhcHBcXFxcYXBpXFxcXHJvdXRlLmpzXCIsXG4gICAgbmV4dENvbmZpZ091dHB1dCxcbiAgICB1c2VybGFuZFxufSk7XG4vLyBQdWxsIG91dCB0aGUgZXhwb3J0cyB0aGF0IHdlIG5lZWQgdG8gZXhwb3NlIGZyb20gdGhlIG1vZHVsZS4gVGhpcyBzaG91bGRcbi8vIGJlIGVsaW1pbmF0ZWQgd2hlbiB3ZSd2ZSBtb3ZlZCB0aGUgb3RoZXIgcm91dGVzIHRvIHRoZSBuZXcgZm9ybWF0LiBUaGVzZVxuLy8gYXJlIHVzZWQgdG8gaG9vayBpbnRvIHRoZSByb3V0ZS5cbmNvbnN0IHsgd29ya0FzeW5jU3RvcmFnZSwgd29ya1VuaXRBc3luY1N0b3JhZ2UsIHNlcnZlckhvb2tzIH0gPSByb3V0ZU1vZHVsZTtcbmZ1bmN0aW9uIHBhdGNoRmV0Y2goKSB7XG4gICAgcmV0dXJuIF9wYXRjaEZldGNoKHtcbiAgICAgICAgd29ya0FzeW5jU3RvcmFnZSxcbiAgICAgICAgd29ya1VuaXRBc3luY1N0b3JhZ2VcbiAgICB9KTtcbn1cbmV4cG9ydCB7IHJvdXRlTW9kdWxlLCB3b3JrQXN5bmNTdG9yYWdlLCB3b3JrVW5pdEFzeW5jU3RvcmFnZSwgc2VydmVySG9va3MsIHBhdGNoRmV0Y2gsICB9O1xuXG4vLyMgc291cmNlTWFwcGluZ1VSTD1hcHAtcm91dGUuanMubWFwIl0sIm5hbWVzIjpbXSwiaWdub3JlTGlzdCI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader/index.js?name=app%2Fapi%2Froute&page=%2Fapi%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Froute.js&appDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard%5Capp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!\n");

/***/ }),

/***/ "(rsc)/./node_modules/next/dist/build/webpack/loaders/next-flight-client-entry-loader.js?server=true!":
/*!******************************************************************************************************!*\
  !*** ./node_modules/next/dist/build/webpack/loaders/next-flight-client-entry-loader.js?server=true! ***!
  \******************************************************************************************************/
/***/ (() => {



/***/ }),

/***/ "(ssr)/./node_modules/next/dist/build/webpack/loaders/next-flight-client-entry-loader.js?server=true!":
/*!******************************************************************************************************!*\
  !*** ./node_modules/next/dist/build/webpack/loaders/next-flight-client-entry-loader.js?server=true! ***!
  \******************************************************************************************************/
/***/ (() => {



/***/ }),

/***/ "(rsc)/./app/api/route.js":
/*!**************************!*\
  !*** ./app/api/route.js ***!
  \**************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   GET: () => (/* binding */ GET),\n/* harmony export */   POST: () => (/* binding */ POST)\n/* harmony export */ });\n/* harmony import */ var next_server__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! next/server */ \"(rsc)/./node_modules/next/dist/api/server.js\");\n/* harmony import */ var jsonwebtoken__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jsonwebtoken */ \"(rsc)/./node_modules/jsonwebtoken/index.js\");\n\n\nasync function POST(req) {\n    const { event, data } = await req.json();\n    const generarToken = ()=>new Promise((resolve, reject)=>{\n            const user = {\n                id: 1,\n                usr: \"factoneta\"\n            };\n            const options = {\n                expiresIn: \"2m\"\n            };\n            jsonwebtoken__WEBPACK_IMPORTED_MODULE_1__.sign(user, \"password123\", options, (error, token)=>{\n                if (error) reject(\"error generando jwt\");\n                resolve(token);\n            });\n        });\n    const verificarToken = (token)=>new Promise((resolve, reject)=>{\n            jsonwebtoken__WEBPACK_IMPORTED_MODULE_1__.verify(token, \"password123\", (error, decoded)=>{\n                if (error) reject(\"error verificando jwt: \" + error);\n                resolve(\"token correcto\");\n            });\n        });\n    switch(event){\n        case 1:\n            try {\n                const { user, password } = data;\n                if (user == \"asd\" && password == \"123\") {\n                    const token = await generarToken();\n                    return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                        login: true,\n                        token\n                    });\n                } else {\n                    return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                        login: false\n                    });\n                }\n            } catch (error) {\n                return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                    error\n                });\n            }\n        case 2:\n            try {\n                return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                    ok: true,\n                    tickets: {\n                        vendidos: 50000,\n                        ingresos: 25000,\n                        adultos: 15000,\n                        menores: 9500,\n                        otros: 500\n                    },\n                    ingresosPorHora: {\n                        \"20:00\": 25000,\n                        \"21:00\": 20000,\n                        \"22:00\": 16000,\n                        \"23:00\": 13000,\n                        \"00:00\": 9000,\n                        \"01:00\": 2000,\n                        \"02:00\": 1000,\n                        \"03:00\": 100,\n                        \"04:00\": 20\n                    }\n                });\n            } catch (error) {\n                return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                    error\n                });\n            }\n        case 3:\n            try {\n                const { token } = data;\n                const r = await verificarToken(token);\n                return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                    r: \"token correcto\"\n                });\n            } catch (error) {\n                return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                    error\n                });\n            }\n        default:\n            return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n                error: \"evento default \"\n            });\n    }\n}\nasync function GET(req) {\n    return next_server__WEBPACK_IMPORTED_MODULE_0__.NextResponse.json({\n        error: \"no get\"\n    });\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9hcHAvYXBpL3JvdXRlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7QUFBMkM7QUFDYjtBQUV2QixlQUFlRSxLQUFPQyxHQUFHO0lBQzVCLE1BQU0sRUFBRUMsS0FBSyxFQUFFQyxJQUFJLEVBQUUsR0FBRyxNQUFNRixJQUFJRyxJQUFJO0lBRXRDLE1BQU1DLGVBQWUsSUFBTSxJQUFJQyxRQUFRLENBQUNDLFNBQVNDO1lBQzdDLE1BQU9DLE9BQU87Z0JBQ1ZDLElBQUk7Z0JBQ0pDLEtBQUs7WUFDVDtZQUNBLE1BQU1DLFVBQVU7Z0JBQ1pDLFdBQVc7WUFDZjtZQUNBZCw4Q0FBUSxDQUFDVSxNQUFNLGVBQWVHLFNBQVMsQ0FBQ0csT0FBT0M7Z0JBQzNDLElBQUdELE9BQU9QLE9BQU87Z0JBQ2pCRCxRQUFRUztZQUNaO1FBQ0o7SUFFQSxNQUFNQyxpQkFBaUIsQ0FBQ0QsUUFBVSxJQUFJVixRQUFRLENBQUNDLFNBQVNDO1lBQ3BEVCxnREFBVSxDQUFDaUIsT0FBTyxlQUFlLENBQUNELE9BQU9JO2dCQUNyQyxJQUFHSixPQUFPUCxPQUFPLDRCQUEwQk87Z0JBQzNDUixRQUFRO1lBQ1o7UUFDSjtJQUVBLE9BQVFMO1FBQ0osS0FBSztZQUNELElBQUk7Z0JBQ0EsTUFBTSxFQUFFTyxJQUFJLEVBQUVXLFFBQVEsRUFBRSxHQUFHakI7Z0JBQzNCLElBQUlNLFFBQVEsU0FBU1csWUFBWSxPQUFPO29CQUNwQyxNQUFNSixRQUFRLE1BQU1YO29CQUNwQixPQUFPUCxxREFBWUEsQ0FBQ00sSUFBSSxDQUFDO3dCQUFFaUIsT0FBTzt3QkFBTUw7b0JBQU07Z0JBQ2xELE9BQU87b0JBQ0gsT0FBT2xCLHFEQUFZQSxDQUFDTSxJQUFJLENBQUM7d0JBQUVpQixPQUFPO29CQUFNO2dCQUM1QztZQUVKLEVBQUUsT0FBT04sT0FBTztnQkFDWixPQUFPakIscURBQVlBLENBQUNNLElBQUksQ0FBQztvQkFBRVc7Z0JBQU07WUFDckM7UUFDSixLQUFLO1lBQ0QsSUFBSTtnQkFDQSxPQUFPakIscURBQVlBLENBQUNNLElBQUksQ0FBQztvQkFDckJrQixJQUFJO29CQUNKQyxTQUFTO3dCQUNMQyxVQUFVO3dCQUNWQyxVQUFVO3dCQUNWQyxTQUFTO3dCQUNUQyxTQUFTO3dCQUNUQyxPQUFPO29CQUNYO29CQUNBQyxpQkFBaUI7d0JBQ2IsU0FBUzt3QkFDVCxTQUFTO3dCQUNULFNBQVM7d0JBQ1QsU0FBUzt3QkFDVCxTQUFTO3dCQUNULFNBQVM7d0JBQ1QsU0FBUzt3QkFDVCxTQUFTO3dCQUNULFNBQVM7b0JBQ2I7Z0JBQ0o7WUFDSixFQUFFLE9BQU9kLE9BQU87Z0JBQ1osT0FBT2pCLHFEQUFZQSxDQUFDTSxJQUFJLENBQUM7b0JBQUVXO2dCQUFNO1lBQ3JDO1FBQ0osS0FBSztZQUNELElBQUk7Z0JBQ0EsTUFBTSxFQUFFQyxLQUFLLEVBQUUsR0FBR2I7Z0JBQ2xCLE1BQU0yQixJQUFJLE1BQU1iLGVBQWVEO2dCQUMvQixPQUFPbEIscURBQVlBLENBQUNNLElBQUksQ0FBQztvQkFBRTBCLEdBQUc7Z0JBQWlCO1lBQ25ELEVBQUUsT0FBT2YsT0FBTztnQkFDWixPQUFPakIscURBQVlBLENBQUNNLElBQUksQ0FBQztvQkFBRVc7Z0JBQU07WUFDckM7UUFFSjtZQUFTLE9BQU9qQixxREFBWUEsQ0FBQ00sSUFBSSxDQUFDO2dCQUFFVyxPQUFPO1lBQWlCO0lBQ2hFO0FBQ0o7QUFFTyxlQUFlZ0IsSUFBTTlCLEdBQUc7SUFDM0IsT0FBT0gscURBQVlBLENBQUNNLElBQUksQ0FBQztRQUFFVyxPQUFPO0lBQVM7QUFDL0MiLCJzb3VyY2VzIjpbIkM6XFxVc2Vyc1xccGF0cmlzaW9cXERlc2t0b3BcXENhcm5hdmFjc1xcZGFzaGJvYXJkXFxhcHBcXGFwaVxccm91dGUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgTmV4dFJlc3BvbnNlIH0gZnJvbSBcIm5leHQvc2VydmVyXCI7XHJcbmltcG9ydCBqd3QgZnJvbSBcImpzb253ZWJ0b2tlblwiXHJcblxyXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gUE9TVCAoIHJlcSApIHtcclxuICAgIGNvbnN0IHsgZXZlbnQsIGRhdGEgfSA9IGF3YWl0IHJlcS5qc29uKClcclxuXHJcbiAgICBjb25zdCBnZW5lcmFyVG9rZW4gPSAoKSA9PiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KT0+e1xyXG4gICAgICAgIGNvbnN0ICB1c2VyID0ge1xyXG4gICAgICAgICAgICBpZDogMSxcclxuICAgICAgICAgICAgdXNyOiBcImZhY3RvbmV0YVwiXHJcbiAgICAgICAgfVxyXG4gICAgICAgIGNvbnN0IG9wdGlvbnMgPSB7XHJcbiAgICAgICAgICAgIGV4cGlyZXNJbjogXCIybVwiXHJcbiAgICAgICAgfVxyXG4gICAgICAgIGp3dC5zaWduKHVzZXIsIFwicGFzc3dvcmQxMjNcIiwgb3B0aW9ucywgKGVycm9yLCB0b2tlbik9PntcclxuICAgICAgICAgICAgaWYoZXJyb3IpIHJlamVjdChcImVycm9yIGdlbmVyYW5kbyBqd3RcIilcclxuICAgICAgICAgICAgcmVzb2x2ZSh0b2tlbilcclxuICAgICAgICB9KVxyXG4gICAgfSlcclxuICAgIFxyXG4gICAgY29uc3QgdmVyaWZpY2FyVG9rZW4gPSAodG9rZW4pID0+IG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpPT57XHJcbiAgICAgICAgand0LnZlcmlmeSh0b2tlbiwgXCJwYXNzd29yZDEyM1wiLCAoZXJyb3IsIGRlY29kZWQpPT57XHJcbiAgICAgICAgICAgIGlmKGVycm9yKSByZWplY3QoXCJlcnJvciB2ZXJpZmljYW5kbyBqd3Q6IFwiK2Vycm9yKVxyXG4gICAgICAgICAgICByZXNvbHZlKFwidG9rZW4gY29ycmVjdG9cIilcclxuICAgICAgICB9KVxyXG4gICAgfSlcclxuXHJcbiAgICBzd2l0Y2ggKGV2ZW50KSB7XHJcbiAgICAgICAgY2FzZSAxOiBcclxuICAgICAgICAgICAgdHJ5IHtcclxuICAgICAgICAgICAgICAgIGNvbnN0IHsgdXNlciwgcGFzc3dvcmQgfSA9IGRhdGFcclxuICAgICAgICAgICAgICAgIGlmKCB1c2VyID09IFwiYXNkXCIgJiYgcGFzc3dvcmQgPT0gXCIxMjNcIikge1xyXG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHRva2VuID0gYXdhaXQgZ2VuZXJhclRva2VuKClcclxuICAgICAgICAgICAgICAgICAgICByZXR1cm4gTmV4dFJlc3BvbnNlLmpzb24oeyBsb2dpbjogdHJ1ZSwgdG9rZW4gfSlcclxuICAgICAgICAgICAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIE5leHRSZXNwb25zZS5qc29uKHsgbG9naW46IGZhbHNlIH0pXHJcbiAgICAgICAgICAgICAgICB9XHJcblxyXG4gICAgICAgICAgICB9IGNhdGNoIChlcnJvcikge1xyXG4gICAgICAgICAgICAgICAgcmV0dXJuIE5leHRSZXNwb25zZS5qc29uKHsgZXJyb3IgfSlcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIGNhc2UgMjogXHJcbiAgICAgICAgICAgIHRyeSB7XHJcbiAgICAgICAgICAgICAgICByZXR1cm4gTmV4dFJlc3BvbnNlLmpzb24oe1xyXG4gICAgICAgICAgICAgICAgICAgIG9rOiB0cnVlLFxyXG4gICAgICAgICAgICAgICAgICAgIHRpY2tldHM6IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgdmVuZGlkb3M6IDUwMDAwLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBpbmdyZXNvczogMjUwMDAsXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGFkdWx0b3M6IDE1MDAwLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBtZW5vcmVzOiA5NTAwLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBvdHJvczogNTAwXHJcbiAgICAgICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgICAgICBpbmdyZXNvc1BvckhvcmE6IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIyMDowMFwiOiAyNTAwMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIyMTowMFwiOiAyMDAwMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIyMjowMFwiOiAxNjAwMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIyMzowMFwiOiAxMzAwMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIwMDowMFwiOiA5MDAwLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBcIjAxOjAwXCI6IDIwMDAsXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIFwiMDI6MDBcIjogMTAwMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgXCIwMzowMFwiOiAxMDAsXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIFwiMDQ6MDBcIjogMjBcclxuICAgICAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICB9KVxyXG4gICAgICAgICAgICB9IGNhdGNoIChlcnJvcikge1xyXG4gICAgICAgICAgICAgICAgcmV0dXJuIE5leHRSZXNwb25zZS5qc29uKHsgZXJyb3IgfSlcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIGNhc2UgMzpcclxuICAgICAgICAgICAgdHJ5IHtcclxuICAgICAgICAgICAgICAgIGNvbnN0IHsgdG9rZW4gfSA9IGRhdGFcclxuICAgICAgICAgICAgICAgIGNvbnN0IHIgPSBhd2FpdCB2ZXJpZmljYXJUb2tlbih0b2tlbilcclxuICAgICAgICAgICAgICAgIHJldHVybiBOZXh0UmVzcG9uc2UuanNvbih7IHI6IFwidG9rZW4gY29ycmVjdG9cIiB9KVxyXG4gICAgICAgICAgICB9IGNhdGNoIChlcnJvcikge1xyXG4gICAgICAgICAgICAgICAgcmV0dXJuIE5leHRSZXNwb25zZS5qc29uKHsgZXJyb3IgfSlcclxuICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICBkZWZhdWx0OiByZXR1cm4gTmV4dFJlc3BvbnNlLmpzb24oeyBlcnJvcjogXCJldmVudG8gZGVmYXVsdCBcIn0pXHJcbiAgICB9XHJcbn1cclxuXHJcbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBHRVQgKCByZXEgKSB7XHJcbiAgICByZXR1cm4gTmV4dFJlc3BvbnNlLmpzb24oeyBlcnJvcjogXCJubyBnZXRcIiB9KVxyXG59Il0sIm5hbWVzIjpbIk5leHRSZXNwb25zZSIsImp3dCIsIlBPU1QiLCJyZXEiLCJldmVudCIsImRhdGEiLCJqc29uIiwiZ2VuZXJhclRva2VuIiwiUHJvbWlzZSIsInJlc29sdmUiLCJyZWplY3QiLCJ1c2VyIiwiaWQiLCJ1c3IiLCJvcHRpb25zIiwiZXhwaXJlc0luIiwic2lnbiIsImVycm9yIiwidG9rZW4iLCJ2ZXJpZmljYXJUb2tlbiIsInZlcmlmeSIsImRlY29kZWQiLCJwYXNzd29yZCIsImxvZ2luIiwib2siLCJ0aWNrZXRzIiwidmVuZGlkb3MiLCJpbmdyZXNvcyIsImFkdWx0b3MiLCJtZW5vcmVzIiwib3Ryb3MiLCJpbmdyZXNvc1BvckhvcmEiLCJyIiwiR0VUIl0sImlnbm9yZUxpc3QiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(rsc)/./app/api/route.js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, ["vendor-chunks/next","vendor-chunks/ms","vendor-chunks/semver","vendor-chunks/jsonwebtoken","vendor-chunks/jws","vendor-chunks/ecdsa-sig-formatter","vendor-chunks/safe-buffer","vendor-chunks/lodash.once","vendor-chunks/lodash.isstring","vendor-chunks/lodash.isplainobject","vendor-chunks/lodash.isnumber","vendor-chunks/lodash.isinteger","vendor-chunks/lodash.isboolean","vendor-chunks/lodash.includes","vendor-chunks/jwa","vendor-chunks/buffer-equal-constant-time"], () => (__webpack_exec__("(rsc)/./node_modules/next/dist/build/webpack/loaders/next-app-loader/index.js?name=app%2Fapi%2Froute&page=%2Fapi%2Froute&appPaths=&pagePath=private-next-app-dir%2Fapi%2Froute.js&appDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard%5Capp&pageExtensions=tsx&pageExtensions=ts&pageExtensions=jsx&pageExtensions=js&rootDir=C%3A%5CUsers%5Cpatrisio%5CDesktop%5CCarnavacs%5Cdashboard&isDev=true&tsconfigPath=tsconfig.json&basePath=&assetPrefix=&nextConfigOutput=&preferredRegion=&middlewareConfig=e30%3D!")));
module.exports = __webpack_exports__;

})();
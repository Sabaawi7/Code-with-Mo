
function dv_rolloutManager(handlersDefsArray, baseHandler) {
    this.handle = function () {
        var errorsArr = [];

        var handler = chooseEvaluationHandler(handlersDefsArray);
        if (handler) {
            var errorObj = handleSpecificHandler(handler);
            if (errorObj === null) {
                return errorsArr;
            }
            else {
                var debugInfo = handler.onFailure();
                if (debugInfo) {
                    for (var key in debugInfo) {
                        if (debugInfo.hasOwnProperty(key)) {
                            if (debugInfo[key] !== undefined || debugInfo[key] !== null) {
                                errorObj[key] = encodeURIComponent(debugInfo[key]);
                            }
                        }
                    }
                }
                errorsArr.push(errorObj);
            }
        }

        var errorObjHandler = handleSpecificHandler(baseHandler);
        if (errorObjHandler) {
            errorObjHandler['dvp_isLostImp'] = 1;
            errorsArr.push(errorObjHandler);
        }
        return errorsArr;
    };

    function handleSpecificHandler(handler) {
        var request;
        var errorObj = null;

        try {
            request = handler.createRequest();
            if (request && !request.isSev1) {
                var url = request.url || request;
                if (url) {
                    if (!handler.sendRequest(url)) {
                        errorObj = createAndGetError('sendRequest failed.',
                            url,
                            handler.getVersion(),
                            handler.getVersionParamName(),
                            handler.dv_script);
                    }
                } else {
                    errorObj = createAndGetError('createRequest failed.',
                        url,
                        handler.getVersion(),
                        handler.getVersionParamName(),
                        handler.dv_script,
                        handler.dvScripts,
                        handler.dvStep,
                        handler.dvOther
                    );
                }
            }
        }
        catch (e) {
            errorObj = createAndGetError(e.name + ': ' + e.message, request ? (request.url || request) : null, handler.getVersion(), handler.getVersionParamName(), (handler ? handler.dv_script : null));
        }

        return errorObj;
    }

    function createAndGetError(error, url, ver, versionParamName, dv_script, dvScripts, dvStep, dvOther) {
        var errorObj = {};
        errorObj[versionParamName] = ver;
        errorObj['dvp_jsErrMsg'] = encodeURIComponent(error);
        if (dv_script && dv_script.parentElement && dv_script.parentElement.tagName && dv_script.parentElement.tagName == 'HEAD') {
            errorObj['dvp_isOnHead'] = '1';
        }
        if (url) {
            errorObj['dvp_jsErrUrl'] = url;
        }
        if (dvScripts) {
            var dvScriptsResult = '';
            for (var id in dvScripts) {
                if (dvScripts[id] && dvScripts[id].src) {
                    dvScriptsResult += encodeURIComponent(dvScripts[id].src) + ":" + dvScripts[id].isContain + ",";
                }
            }
            
            
            
        }
        return errorObj;
    }

    function chooseEvaluationHandler(handlersArray) {
        var config = window._dv_win.dv_config;
        var index = 0;
        var isEvaluationVersionChosen = false;
        if (config.handlerVersionSpecific) {
            for (var i = 0; i < handlersArray.length; i++) {
                if (handlersArray[i].handler.getVersion() == config.handlerVersionSpecific) {
                    isEvaluationVersionChosen = true;
                    index = i;
                    break;
                }
            }
        }
        else if (config.handlerVersionByTimeIntervalMinutes) {
            var date = config.handlerVersionByTimeInputDate || new Date();
            var hour = date.getUTCHours();
            var minutes = date.getUTCMinutes();
            index = Math.floor(((hour * 60) + minutes) / config.handlerVersionByTimeIntervalMinutes) % (handlersArray.length + 1);
            if (index != handlersArray.length) { 
                isEvaluationVersionChosen = true;
            }
        }
        else {
            var rand = config.handlerVersionRandom || (Math.random() * 100);
            for (var i = 0; i < handlersArray.length; i++) {
                if (rand >= handlersArray[i].minRate && rand < handlersArray[i].maxRate) {
                    isEvaluationVersionChosen = true;
                    index = i;
                    break;
                }
            }
        }

        if (isEvaluationVersionChosen == true && handlersArray[index].handler.isApplicable()) {
            return handlersArray[index].handler;
        }
        else {
            return null;
        }
    }
}

function doesBrowserSupportHTML5Push() {
    "use strict";
    return typeof window.parent.postMessage === 'function' && window.JSON;
}

function dv_GetParam(url, name, checkFromStart) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = (checkFromStart ? "(?:\\?|&|^)" : "[\\?&]") + name + "=([^&#]*)";
    var regex = new RegExp(regexS, 'i');
    var results = regex.exec(url);
    if (results == null)
        return null;
    else
        return results[1];
}

function dv_Contains(array, obj) {
    var i = array.length;
    while (i--) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
}

function dv_GetDynamicParams(url, prefix) {
    try {
        prefix = (prefix != undefined && prefix != null) ? prefix : 'dvp';
        var regex = new RegExp("[\\?&](" + prefix + "_[^&]*=[^&#]*)", "gi");
        var dvParams = regex.exec(url);

        var results = [];
        while (dvParams != null) {
            results.push(dvParams[1]);
            dvParams = regex.exec(url);
        }
        return results;
    }
    catch (e) {
        return [];
    }
}

function dv_createIframe() {
    var iframe;
    if (document.createElement && (iframe = document.createElement('iframe'))) {
        iframe.name = iframe.id = 'iframe_' + Math.floor((Math.random() + "") * 1000000000000);
        iframe.width = 0;
        iframe.height = 0;
        iframe.style.display = 'none';
        iframe.src = 'about:blank';
    }

    return iframe;
}

function dv_GetRnd() {
    return ((new Date()).getTime() + "" + Math.floor(Math.random() * 1000000)).substr(0, 16);
}

function dv_SendErrorImp(serverUrl, errorsArr) {

    for (var j = 0; j < errorsArr.length; j++) {
        var errorObj = errorsArr[j];
        var errorImp =   dv_CreateAndGetErrorImp(serverUrl, errorObj);
        dv_sendImgImp(errorImp);
    }
}

function dv_CreateAndGetErrorImp(serverUrl, errorObj) {
    var errorQueryString = '';
    for (key in errorObj) {
        if (errorObj.hasOwnProperty(key)) {
            if (key.indexOf('dvp_jsErrUrl') == -1) {
                errorQueryString += '&' + key + '=' + errorObj[key];
            }
            else {
                var params = ['ctx', 'cmp', 'plc', 'sid'];
                for (var i = 0; i < params.length; i++) {
                    var pvalue = dv_GetParam(errorObj[key], params[i]);
                    if (pvalue) {
                        errorQueryString += '&dvp_js' + params[i] + '=' + pvalue;
                    }
                }
            }
        }
    }

    var sslFlag = '&ssl=1';
    var errorImp = 'https://' + serverUrl + sslFlag + errorQueryString;

    return errorImp;
}

function dv_getDVUniqueKey(elm) {
    return elm && elm.getAttribute('data-uk');
}

function dv_getDVErrorGlobalScope(elm) {
    var uniqueKey = dv_getDVUniqueKey(elm);
    return uniqueKey && window._dv_win && window._dv_win[uniqueKey] && window._dv_win[uniqueKey].globalScopeVerifyErrorHandler || {};
}

function dv_onLoad(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        var scriptSRC = dv_getScriptSRC(elm);
        if (!globalScope.isJSONPCalled) {
            setTimeout(function onTimeout(){
                globalScope.onTimeout(scriptSRC);
            }, globalScope.msTillJSONPCalled);
        }
    }
}

function dv_onResponse(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        var scriptSRC = dv_getScriptSRC(elm);
        if (!globalScope.isJSONPCalled) {
            globalScope.onResponse(scriptSRC);
        }
    }
}

function dv_getScriptSRC(elm) {
    return elm && elm.src || '';
}
var IQPAParams = [
    "auprice", "ppid", "audeal", "auevent", "auadv", "aucmp", "aucrtv", "auorder", "ausite", "auplc", "auxch", "audvc", "aulitem",
    "auadid", "pltfrm", "aufilter1", "aufilter2", "autt", "auip", "aubndl", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9",
    "c10", "c11", "c12", "c13", "c14", "c15"
];

function dv_AppendIQPAParams(src) {
    var qs = [];
    var paramVal;
    IQPAParams.forEach(function forEachParam(paramName){
        paramVal = dv_GetParam(src, paramName);
        if (paramVal !== '' && paramVal !== null) {
            qs.push([paramName, paramVal].join('='));
        }
    });
    return qs.length && '&' + qs.join('&') || '';
}

function dv_onError(evt) {
    var elm = evt && evt.target || {};
    var globalScope = dv_getDVErrorGlobalScope(elm);
    if (globalScope) {
        globalScope.onError(dv_getScriptSRC(elm));
    }
}

function dv_getDVBSErrAddress(config) {
    return config && config.bsErrAddress || 'rtb0.doubleverify.com';
}

function dv_sendImgImp(url) {
    (new Image()).src = url;
}

function dv_sendScriptRequest(url, onLoad, onError, uniqueKey) {
    var emptyFunction = function(){};
    onLoad = onLoad || emptyFunction;
    onError = onError || emptyFunction;
    document.write('<scr' + 'ipt data-uk="' + uniqueKey + '" onerror="(' + onError + ')({target:this});" onload="(' + onLoad + ')({target:this});" type="text/javascript" src="' + url + '"></scr' + 'ipt>');
}

function dv_getPropSafe(obj, propName) {
    try {
        if (obj)
            return obj[propName];
    } catch (e) {
    }
}

function dvBsType() {
    var that = this;
    var eventsForDispatch = {};

    this.getEventsForDispatch = function getEventsForDispatch () {
        return eventsForDispatch;
    };

    var messageEventListener = function (event) {
        try {
            var timeCalled = getCurrentTime();
            var data = window.JSON.parse(event.data);
            if (!data.action) {
                data = window.JSON.parse(data);
            }
            if (data.timeStampCollection) {
                data.timeStampCollection.push({messageEventListenerCalled: timeCalled});
            }
            var myUID;
            var visitJSHasBeenCalledForThisTag = false;
            if ($dvbs.tags) {
                for (var uid in $dvbs.tags) {
                    if ($dvbs.tags.hasOwnProperty(uid) && $dvbs.tags[uid] && $dvbs.tags[uid].t2tIframeId === data.iFrameId) {
                        myUID = uid;
                        visitJSHasBeenCalledForThisTag = true;
                        break;
                    }
                }
            }

        } catch (e) {
            try {
                dv_SendErrorImp(window._dv_win.dv_config.tpsErrAddress + '/visit.jpg?flvr=0&ctx=818052&cmp=1619415&dvtagver=6.1.src&jsver=0&dvp_ist2tListener=1', {dvp_jsErrMsg: encodeURIComponent(e)});
            } catch (ex) {
            }
        }
    };

    if (window.addEventListener)
        addEventListener("message", messageEventListener, false);
    else
        attachEvent("onmessage", messageEventListener);

    this.pubSub = new function () {

        var subscribers = [];

        this.subscribe = function (eventName, uid, actionName, func) {
            if (!subscribers[eventName + uid])
                subscribers[eventName + uid] = [];
            subscribers[eventName + uid].push({Func: func, ActionName: actionName});
        };

        this.publish = function (eventName, uid) {
            var actionsResults = [];
            if (eventName && uid && subscribers[eventName + uid] instanceof Array)
                for (var i = 0; i < subscribers[eventName + uid].length; i++) {
                    var funcObject = subscribers[eventName + uid][i];
                    if (funcObject && funcObject.Func && typeof funcObject.Func == "function" && funcObject.ActionName) {
                        var isSucceeded = runSafely(function () {
                            return funcObject.Func(uid);
                        });
                        actionsResults.push(encodeURIComponent(funcObject.ActionName) + '=' + (isSucceeded ? '1' : '0'));
                    }
                }
            return actionsResults.join('&');
        };
    };

    this.domUtilities = new function () {

        this.addImage = function (url, parentElement, trackingPixelCompleteCallbackName) {
            url = appendCacheBuster(url);
            if (typeof(navigator.sendBeacon) === 'function') {
                var isSuccessfullyQueuedDataForTransfer = navigator.sendBeacon(url);
                if (isSuccessfullyQueuedDataForTransfer && typeof(window[trackingPixelCompleteCallbackName]) === 'function') {
                    window[trackingPixelCompleteCallbackName]();
                }
                return;
            }

            var image = new Image();
            if (typeof(window[trackingPixelCompleteCallbackName]) === 'function') {
                image.addEventListener('load', window[trackingPixelCompleteCallbackName]);
            }
            image.src = url;
        };

        this.addScriptResource = function (url, parentElement, onLoad, onError, uniqueKey) {
            var emptyFunction = function(){};
            onLoad = onLoad || emptyFunction;
            onError = onError || emptyFunction;
            uniqueKey = uniqueKey || '';
            if (parentElement) {
                var scriptElem = parentElement.ownerDocument.createElement("script");
                scriptElem.onerror = onError;
                scriptElem.onload = onLoad;
                if (scriptElem && typeof(scriptElem.setAttribute) === 'function') {
                    scriptElem.setAttribute('data-uk', uniqueKey);
                }
                scriptElem.type = 'text/javascript';
                scriptElem.src = appendCacheBuster(url);
                parentElement.insertBefore(scriptElem, parentElement.firstChild);
            }
            else {
                addScriptResourceFallBack(url, onLoad, onError, uniqueKey);
            }
        };

        function addScriptResourceFallBack(url, onLoad, onError, uniqueKey) {
            var emptyFunction = function(){};
            onLoad = onLoad || emptyFunction;
            onError = onError || emptyFunction;
            uniqueKey = uniqueKey || '';
            var scriptElem = document.createElement('script');
            scriptElem.onerror = onError;
            scriptElem.onload = onLoad;
            if (scriptElem && typeof(scriptElem.setAttribute) === 'function') {
                scriptElem.setAttribute('data-uk', uniqueKey);
            }
            scriptElem.type = "text/javascript";
            scriptElem.src = appendCacheBuster(url);
            var firstScript = document.getElementsByTagName('script')[0];
            firstScript.parentNode.insertBefore(scriptElem, firstScript);
        }

        this.addScriptCode = function (srcCode, parentElement) {
            var scriptElem = parentElement.ownerDocument.createElement("script");
            scriptElem.type = 'text/javascript';
            scriptElem.innerHTML = srcCode;
            parentElement.insertBefore(scriptElem, parentElement.firstChild);
        };

        this.addHtml = function (srcHtml, parentElement) {
            var divElem = parentElement.ownerDocument.createElement("div");
            divElem.style = "display: inline";
            divElem.innerHTML = srcHtml;
            parentElement.insertBefore(divElem, parentElement.firstChild);
        };
    };

    this.resolveMacros = function (str, tag) {
        var viewabilityData = tag.getViewabilityData();
        var viewabilityBuckets = viewabilityData && viewabilityData.buckets ? viewabilityData.buckets : {};
        var upperCaseObj = objectsToUpperCase(tag, viewabilityData, viewabilityBuckets);
        var newStr = str.replace('[DV_PROTOCOL]', upperCaseObj.DV_PROTOCOL);
        newStr = newStr.replace('[PROTOCOL]', upperCaseObj.PROTOCOL);
        newStr = newStr.replace(/\[(.*?)\]/g, function (match, p1) {
            var value = upperCaseObj[p1];
            if (value === undefined || value === null)
                value = '[' + p1 + ']';
            return encodeURIComponent(value);
        });
        return newStr;
    };

    this.settings = new function () {
    };

    this.tagsType = function () {
    };

    this.tagsPrototype = function () {
        this.add = function (tagKey, obj) {
            if (!that.tags[tagKey])
                that.tags[tagKey] = new that.tag();
            for (var key in obj)
                that.tags[tagKey][key] = obj[key];
        };
    };

    this.tagsType.prototype = new this.tagsPrototype();
    this.tagsType.prototype.constructor = this.tags;
    this.tags = new this.tagsType();

    this.tag = function () {
    };
    this.tagPrototype = function () {
        this.set = function (obj) {
            for (var key in obj)
                this[key] = obj[key];
        };

        this.getViewabilityData = function () {
        };
    };

    this.tag.prototype = new this.tagPrototype();
    this.tag.prototype.constructor = this.tag;

    this.getTagObjectByService = function (serviceName) {

        for (var impressionId in this.tags) {
            if (typeof this.tags[impressionId] === 'object'
                && this.tags[impressionId].services
                && this.tags[impressionId].services[serviceName]
                && !this.tags[impressionId].services[serviceName].isProcessed) {
                this.tags[impressionId].services[serviceName].isProcessed = true;
                return this.tags[impressionId];
            }
        }


        return null;
    };

    this.addService = function (impressionId, serviceName, paramsObject) {

        if (!impressionId || !serviceName)
            return;

        if (!this.tags[impressionId])
            return;
        else {
            if (!this.tags[impressionId].services)
                this.tags[impressionId].services = {};

            this.tags[impressionId].services[serviceName] = {
                params: paramsObject,
                isProcessed: false
            };
        }
    };

    this.Enums = {
        BrowserId: {Others: 0, IE: 1, Firefox: 2, Chrome: 3, Opera: 4, Safari: 5},
        TrafficScenario: {OnPage: 1, SameDomain: 2, CrossDomain: 128}
    };

    this.CommonData = {};

    var runSafely = function (action) {
        try {
            var ret = action();
            return ret !== undefined ? ret : true;
        } catch (e) {
            return false;
        }
    };

    var objectsToUpperCase = function () {
        var upperCaseObj = {};
        for (var i = 0; i < arguments.length; i++) {
            var obj = arguments[i];
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    upperCaseObj[key.toUpperCase()] = obj[key];
                }
            }
        }
        return upperCaseObj;
    };

    var appendCacheBuster = function (url) {
        if (url !== undefined && url !== null && url.match("^http") == "http") {
            if (url.indexOf('?') !== -1) {
                if (url.slice(-1) == '&')
                    url += 'cbust=' + dv_GetRnd();
                else
                    url += '&cbust=' + dv_GetRnd();
            }
            else
                url += '?cbust=' + dv_GetRnd();
        }
        return url;
    };

    
    var messagesClass = function () {
        var waitingMessages = [];

        this.registerMsg = function(dvFrame, data) {
            if (!waitingMessages[dvFrame.$frmId]) {
                waitingMessages[dvFrame.$frmId] = [];
            }

            waitingMessages[dvFrame.$frmId].push(data);

            if (dvFrame.$uid) {
                sendWaitingEventsForFrame(dvFrame, dvFrame.$uid);
            }
        };

        this.startSendingEvents = function(dvFrame, impID) {
            sendWaitingEventsForFrame(dvFrame, impID);
            
        };

        function sendWaitingEventsForFrame(dvFrame, impID) {
            if (waitingMessages[dvFrame.$frmId]) {
                var eventObject = {};
                for (var i = 0; i < waitingMessages[dvFrame.$frmId].length; i++) {
                    var obj = waitingMessages[dvFrame.$frmId].pop();
                    for (var key in obj) {
                        if (typeof obj[key] !== 'function' && obj.hasOwnProperty(key)) {
                            eventObject[key] = obj[key];
                        }
                    }
                }
                that.registerEventCall(impID, eventObject);
            }
        }

        function startMessageManager() {
            for (var frm in waitingMessages) {
                if (frm && frm.$uid) {
                    sendWaitingEventsForFrame(frm, frm.$uid);
                }
            }
            setTimeout(startMessageManager, 10);
        }
    };
    this.messages = new messagesClass();

    this.dispatchRegisteredEventsFromAllTags = function () {
        for (var impressionId in this.tags) {
            if (typeof this.tags[impressionId] !== 'function' && typeof this.tags[impressionId] !== 'undefined')
                dispatchEventCalls(impressionId, this);
        }
    };

    var dispatchEventCalls = function (impressionId, dvObj) {
        var tag = dvObj.tags[impressionId];
        var eventObj = eventsForDispatch[impressionId];
        if (typeof eventObj !== 'undefined' && eventObj != null) {
            var url = 'https://' + tag.ServerPublicDns + "/bsevent.gif?flvr=0&impid=" + impressionId + '&' + createQueryStringParams(eventObj);
            dvObj.domUtilities.addImage(url, tag.tagElement.parentElement);
            eventsForDispatch[impressionId] = null;
        }
    };

    this.registerEventCall = function (impressionId, eventObject, timeoutMs) {
        addEventCallForDispatch(impressionId, eventObject);

        if (typeof timeoutMs === 'undefined' || timeoutMs == 0 || isNaN(timeoutMs))
            dispatchEventCallsNow(this, impressionId, eventObject);
        else {
            if (timeoutMs > 2000)
                timeoutMs = 2000;

            var dvObj = this;
            setTimeout(function () {
                dispatchEventCalls(impressionId, dvObj);
            }, timeoutMs);
        }
    };

    this.createEventCallUrl = function(impId, eventObject) {
        var tag = this.tags && this.tags[impId];
        if (tag && typeof eventObject !== 'undefined' && eventObject !== null) {
            return ['https://', tag.ServerPublicDns, '/bsevent.gif?flvr=0&impid=', impId, '&', createQueryStringParams(eventObject)].join('');
        }
    }

    var dispatchEventCallsNow = function (dvObj, impressionId, eventObject) {
        addEventCallForDispatch(impressionId, eventObject);
        dispatchEventCalls(impressionId, dvObj);
    };

    var addEventCallForDispatch = function (impressionId, eventObject) {
        for (var key in eventObject) {
            if (typeof eventObject[key] !== 'function' && eventObject.hasOwnProperty(key)) {
                if (!eventsForDispatch[impressionId])
                    eventsForDispatch[impressionId] = {};
                eventsForDispatch[impressionId][key] = eventObject[key];
            }
        }
    };

    if (window.addEventListener) {
        window.addEventListener('unload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
        window.addEventListener('beforeunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
    }
    else if (window.attachEvent) {
        window.attachEvent('onunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
        window.attachEvent('onbeforeunload', function () {
            that.dispatchRegisteredEventsFromAllTags();
        }, false);
    }
    else {
        window.document.body.onunload = function () {
            that.dispatchRegisteredEventsFromAllTags();
        };
        window.document.body.onbeforeunload = function () {
            that.dispatchRegisteredEventsFromAllTags();
        };
    }

    var createQueryStringParams = function (values) {
        var params = '';
        for (var key in values) {
            if (typeof values[key] !== 'function') {
                var value = encodeURIComponent(values[key]);
                if (params === '')
                    params += key + '=' + value;
                else
                    params += '&' + key + '=' + value;
            }
        }

        return params;
    };
}


function dv_baseHandler(){function M(b){var c=window._dv_win,f=0;try{for(;10>f;){if(c[b]&&"object"===typeof c[b])return!0;if(c==c.parent)break;f++;c=c.parent}}catch(e){}return!1}function G(b){var c=0,f;for(f in b)b.hasOwnProperty(f)&&++c;return c}function N(b,c){a:{var f={};try{if(b&&b.performance&&b.performance.getEntries){var e=b.performance.getEntries();for(b=0;b<e.length;b++){var d=e[b],l=d.name.match(/.*\/(.+?)\./);if(l&&l[1]){var g=l[1].replace(/\d+$/,""),h=c[g];if(h){for(var u=0;u<h.stats.length;u++){var q=
h.stats[u];f[h.prefix+q.prefix]=Math.round(d[q.name])}delete c[g];if(!G(c))break}}}}var n=f;break a}catch(y){}n=void 0}if(n&&G(n))return n}function O(b,c){function f(b){var d=q,c;for(c in b)b.hasOwnProperty(c)&&(d+=["&"+c,"="+b[c]].join(""));return d}function e(){return Date.now?Date.now():(new Date).getTime()}function d(){if(!C){C=!0;var d=f({dvp_injd:1});$dvbs.domUtilities.addImage(d,document.body);d="https://cdn.doubleverify.com/dvtp_src.js#tagtype=video";var c="ctx cmp plc sid adsrv adid crt advid prr dup turl iframe ad vssd apifw vstvr tvcp ppid auip pltfrm gdpr gdpr_consent adu invs litm ord sadv scrt vidreg seltag splc spos sup unit dvtagver msrapi vfwctx auprice audeal auevent auadv aucmp aucrtv auorder ausite auplc auxch audvc aulitem auadid autt c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 aufilter1 aufilter2 ppid".split(" ");
for(i=0;i<c.length;i++){var g=c[i],l=h(b,g);void 0!==l&&(d+=["&",g,"=",encodeURIComponent(l)].join(""))}d+="&gmnpo="+("1"==b.gmnpo?"1":"0");d+="&dvp_dvtpts="+e();d+="&bsimpid="+u;void 0!==b.dvp_aubndl&&(d+="&aubndl="+encodeURIComponent(b.dvp_aubndl));for(var n in b)b.hasOwnProperty(n)&&n.match(/^dvpx?_/i)&&b[n]&&(d+=["&",n.toLocaleLowerCase(),"=",encodeURIComponent(b[n])].join(""));$dvbs.domUtilities.addScriptResource(d,document.body)}}function l(b){var d={};d[b]=e();b=f(d);$dvbs.domUtilities.addImage(b,
document.body)}function g(b,d){-1<t.indexOf(b)?l(d):x.subscribe(function(){l(d)},b)}function h(b,d){d=d.toLowerCase();for(tmpKey in b)if(tmpKey.toLowerCase()===d)return b[tmpKey];return null}var u=b.impressionId,q=window._dv_win.dv_config.bsEventJSURL?window._dv_win.dv_config.bsEventJSURL:"https://"+b.ServerPublicDns+"/bsevent.gif";q+="?flvr=0&impid="+encodeURIComponent(u);var n=f({dvp_innovidImp:1}),y="responseReceived_"+u,p=b.DVP_DCB||b.DVP_DECISION_CALLBACK,m=h(b,"adid"),r=function(b){var d=b;
switch(b){case 5:d=1;break;case 6:d=2}return d}(c.ResultID),C=!1;$dvbs.domUtilities.addImage(n,document.body);if("function"===typeof window[p]){var v=!1;setTimeout(function(){var b=f({dvp_wasCallbackCalled:v});$dvbs.domUtilities.addImage(b,document.body)},1E3);window[y]=function(b,c,g,l,h,n,m){v=!0;try{if(m){var k=f({dvp_stat:m});$dvbs.domUtilities.addImage(k,document.body)}else{k=f({dvp_r9:e()});$dvbs.domUtilities.addImage(k,document.body);g="&dvp_cStartTS="+g+"&dvp_cEndTS="+l+"&dvp_dReceivedTS="+
h+"&dvp_wasAdPlayed="+b;l=r;if(!c)switch(l=2,r){case 1:var p=21;break;case 2:p=20;break;case 3:p=22;break;case 4:p=23}c={bres:l,dvp_blkDecUsed:c?"1":"0"};p&&(c.breason=p);k=f(c)+g;$dvbs.domUtilities.addImage(k,document.body,n);b&&!checkIsOvv()&&d()}}catch(P){b=f({dvp_innovidCallbackEx:1,dvp_innovidCallbackExMsg:P}),$dvbs.domUtilities.addImage(b,document.body)}};try{var z=f({dvp_r8:e()});$dvbs.domUtilities.addImage(z,document.body);window[p](r,y)}catch(w){c=f({dvp_innovidEx:1,dvp_innovidExMsg:w}),
$dvbs.domUtilities.addImage(c,document.body)}}else c=f({dvp_innovidNoCallback:1}),$dvbs.domUtilities.addImage(c,document.body);try{var x=window[m]();if(x.getPreviousEvents&&"function"===typeof x.getPreviousEvents){z=f({dvp_r10:e()});$dvbs.domUtilities.addImage(z,document.body);var t=x.getPreviousEvents(),k=0;-1<t.indexOf("AdStarted")?(k=1,d()):x.subscribe(d,"AdStarted");z=f({dvp_innovidAdStarted:k,dvp_innovidPrevEvents:t});$dvbs.domUtilities.addImage(z,document.body);g("AdError","dvp_ader");g("AdStopped",
"dvp_adst");g("AdVideoStart","dvp_avse");g("AdImpression","dvp_aie")}else k=f({dvp_innovidCallbackEx:3,dvp_innovidCallbackExMsg:"vpaidWrapper.getPreviousEvents not a function"}),$dvbs.domUtilities.addImage(k,document.body)}catch(w){k=f({dvp_innovidCallbackEx:2,dvp_innovidCallbackExMsg:w,dvp_adid:m}),$dvbs.domUtilities.addImage(k,document.body)}}function Q(b){var c,f=window._dv_win.document.visibilityState;window[b.tagObjectCallbackName]=function(e){var d=window._dv_win.$dvbs;d&&(c=e.ImpressionID,
d.tags.add(e.ImpressionID,b),d.tags[e.ImpressionID].set({tagElement:b.script,impressionId:e.ImpressionID,dv_protocol:b.protocol,protocol:"https:",uid:b.uid,serverPublicDns:e.ServerPublicDns,ServerPublicDns:e.ServerPublicDns}),b.script&&b.script.dvFrmWin&&(b.script.dvFrmWin.$uid=e.ImpressionID,d.messages&&d.messages.startSendingEvents&&d.messages.startSendingEvents(b.script.dvFrmWin,e.ImpressionID)),function(){function b(){var c=window._dv_win.document.visibilityState;"prerender"===f&&"prerender"!==
c&&"unloaded"!==c&&(f=c,window._dv_win.$dvbs.registerEventCall(e.ImpressionID,{prndr:0}),window._dv_win.document.removeEventListener(d,b))}if("prerender"===f)if("prerender"!==window._dv_win.document.visibilityState&&"unloaded"!==visibilityStateLocal)window._dv_win.$dvbs.registerEventCall(e.ImpressionID,{prndr:0});else{var d;"undefined"!==typeof window._dv_win.document.hidden?d="visibilitychange":"undefined"!==typeof window._dv_win.document.mozHidden?d="mozvisibilitychange":"undefined"!==typeof window._dv_win.document.msHidden?
d="msvisibilitychange":"undefined"!==typeof window._dv_win.document.webkitHidden&&(d="webkitvisibilitychange");window._dv_win.document.addEventListener(d,b,!1)}}());if("1"!=b.foie)try{var l=N(window,{verify:{prefix:"vf",stats:[{name:"duration",prefix:"dur"}]}});l&&window._dv_win.$dvbs.registerEventCall(e.ImpressionID,l)}catch(g){}};window[b.callbackName]=function(e){A.setIsJSONPCalled(!0);var d=window._dv_win.$dvbs&&"object"==typeof window._dv_win.$dvbs.tags[c]?window._dv_win.$dvbs.tags[c]:b;var f=
window._dv_win.dv_config.bs_renderingMethod||function(b){document.write(b)};"2"!=d.tagformat||void 0===d.DVP_DCB&&void 0===d.DVP_DECISION_CALLBACK||O(d,e);switch(e.ResultID){case 1:d.tagPassback?f(d.tagPassback):e.Passback?f(decodeURIComponent(e.Passback)):e.AdWidth&&e.AdHeight&&f(decodeURIComponent("%3Cdiv%20style%3D%22display%3A%20flex%3B%20align-items%3A%20center%3B%20justify-content%3A%20center%3B%20width%3A%20"+e.AdWidth+"px%3B%20height%3A%20"+e.AdHeight+"px%3B%20outline-offset%3A%20-1px%3B%20background%3A%20url('data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAADoAAAA6CAYAAAGWvHq%2BAAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5AQBECEbFuFN7gAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAFBklEQVRo3uUby3arOEzxAbxIyKLt%2F%2F9gIQtIF4aFZ5ERVxhJyIbcnjmjTZLast4vQ%2BG762OMMX53fQzTFIfxGenfKvgXvj4%2FoOsfy3eECgBgmmcYhnFZ6PoHeO%2F%2FbBiGEQAAxufPghlC%2BLOBYqa%2FHezAJcYYOUz87QAA7vd2g4lMAsrLfQJ%2BQeUM43PZsMJEwN8L58gMfgIAAMVKv6syX4bxGVF9qTiuvV2Byouf7e0Kl%2B%2Buj6kJU8aktV07aFClTkThfm9hGMbNGu53dCNd%2FPr8gBCm5TsnAivz%2BPwBqkHvPaDiVvpAW6Nh0FBhmpagSdfQV0Q7oVySPrz3LyO3t%2BvCKrJIHTtdG58%2FvLycZk%2Bzr1uFkgFWuYHKZHHNEMIr4lMb0pO5v7e3qyyj983KATYydv1jswFZneZ5wzaKVaEMVnNgjsw2B8pcbMdLmKbY1PVG5dTl0rVpnsGlSDReOcfo%2Bgc0df3SagrTPC8m4aDrH1ClaR4AgHKRmgN%2FL9HBbeI4wdKVitXUtYpLGXPSgpUg1lBaPzWCWW6wJ4lkB9aFUL1pQkXOvW9WBDltULNM8wwhTEtIcQn88t31kdpEU7FmOwsemqiiqtPsQvufXMCmCulUSKy9XaG9XYGrLhbv1iSlWU0NGdyQqlPKBHQfh0vxVkQ1abSQybX3oQ7nUPWUpEQ1oaokLVAnSfG4cy8xxpjrEFyVtuCJNt3rETDgu%2F6xiT9zRqKSci0DxzHdZ5E0zXabjGTtwSxr9FyqjazSJkmTi%2Bckb01BS5HaGnems%2BZWzdb62qQTfQdwDDl2Wj0RuKnYpX1sDrJljcvHTqow4%2FNn5SBNXYuzPD0Y8agDsRlpr3NIg1vyYGnSS%2BPUURVIcRhC2A0ZyYPxTKqNyuo8IYRlpMSGLYRJDRdOYyEEqEpDIIfY5qYhhLBrL0s%2BLS7imqq995tijYVdCxlx0EMnaW9XlvD93m4aZ0s4cZ3gqspYOjppRKcMcXipGZyU7Ju63iXIhVOKx53trCWqtMpwZzor8n%2BqynBnnlJlNGa5M51VSmlksBSDlOHlKk%2FzUq0KcVVEYgidytz3coS19lPrFh1y2fUP1Xu1HKsRxHWakao9hLNglZHeESaal3vvocKx3zKP7BXnLJtaxgNkjKY1Wp1y7inYUVG7Akg79vSeKefKwHJ1kEtTikBxJrYkmpIBr1TgPdgbrZ1WkPbuz84UEiNZG1ZLhdydE0sqeqlytGG2pEt4%2B0Ccc9H8zs4kS1Br0542F0fqR0lesOCwyehoIioZq86gqcWq6XbZwrTGqMSAhmOhKWVpjp74PObIsLt3R3g0g1oETs8R32woFbLEHUuEs9CiZa6SslZJmpcuf%2F4GcNc0tDf9lYcxvwGVrI3mkDVeY0NjbumOui9XCtkYlZJIbjt3pF8tzQ0czZTvTXnJSdlHSstRXAlPUpQ4vRy1TK4nnNEwaDTd2ZNE6fQSQiieevBiprjXLamjpco5Mv1YSuH%2Fpry4o%2BMPN70cgZI4tYyG7h3J4evzI1tJ%2BIynBLTHMdnlpXQKsTQCkoAaPakZEctL%2BpbK0Y7FMkloCnrXHMsKileMpS0ZR3zvveez2kDJG6szRiSuJqaulfbOaQJ5KfcYH5wnLK82v2uMCmHaPDz%2BDVj%2BfSNNBGdZmIu9v6EIKWbVZHTmVYrl9clSRVsS0urOKDdlW1J%2B6SubFoH3SiF13X8A3uobUgsAG3MAAAAASUVORK5CYII%3D')%20repeat%3B%20outline%3A%20solid%201px%20%23969696%3B%22%3E%3C%2Fdiv%3E"));
break;case 2:case 3:d.tagAdtag&&f(d.tagAdtag);break;case 4:e.AdWidth&&e.AdHeight&&f(decodeURIComponent("%3Cstyle%3E%0A.dvbs_container%20%7B%0A%09border%3A%201px%20solid%20%233b599e%3B%0A%09overflow%3A%20hidden%3B%0A%09filter%3A%20progid%3ADXImageTransform.Microsoft.gradient(startColorstr%3D%27%23315d8c%27%2C%20endColorstr%3D%27%2384aace%27)%3B%0A%7D%0A%3C%2Fstyle%3E%0A%3Cdiv%20class%3D%22dvbs_container%22%20style%3D%22width%3A%20"+e.AdWidth+"px%3B%20height%3A%20"+e.AdHeight+"px%3B%22%3E%09%0A%3C%2Fdiv%3E"))}}}
function R(b){var c=null,f=null,e=function(b){var d=dv_GetParam(b,"cmp");b=dv_GetParam(b,"ctx");return"919838"==b&&"7951767"==d||"919839"==b&&"7939985"==d||"971108"==b&&"7900229"==d||"971108"==b&&"7951940"==d?"</scr'+'ipt>":/<\/scr\+ipt>/g}(b.src);"function"!==typeof String.prototype.trim&&(String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")});var d=function(b){!(b=b.previousSibling)||"#text"!=b.nodeName||null!=b.nodeValue&&void 0!=b.nodeValue&&0!=b.nodeValue.trim().length||(b=b.previousSibling);
if(b&&"SCRIPT"==b.tagName&&b.getAttribute("type")&&("text/adtag"==b.getAttribute("type").toLowerCase()||"text/passback"==b.getAttribute("type").toLowerCase())&&""!=b.innerHTML.trim()){if("text/adtag"==b.getAttribute("type").toLowerCase())return c=b.innerHTML.replace(e,"\x3c/script>"),{isBadImp:!1,hasPassback:!1,tagAdTag:c,tagPassback:f};if(null!=f)return{isBadImp:!0,hasPassback:!1,tagAdTag:c,tagPassback:f};f=b.innerHTML.replace(e,"\x3c/script>");b=d(b);b.hasPassback=!0;return b}return{isBadImp:!0,
hasPassback:!1,tagAdTag:c,tagPassback:f}};return d(b)}function I(b,c,f,e,d,l,g,h,u,q,n,y){c.dvregion=0;var p=dv_GetParam(k,"useragent");k=window._dv_win.$dvbs.CommonData;if(void 0!=k.BrowserId&&void 0!=k.BrowserVersion&&void 0!=k.BrowserIdFromUserAgent)var m={ID:k.BrowserId,version:k.BrowserVersion,ID_UA:k.BrowserIdFromUserAgent};else m=S(p?decodeURIComponent(p):navigator.userAgent),k.BrowserId=m.ID,k.BrowserVersion=m.version,k.BrowserIdFromUserAgent=m.ID_UA;var r="";void 0!=c.aUrl&&(r="&aUrl="+c.aUrl);
var C="";try{e.depth=T(e);var v=U(e,f,m);if(v&&v.duration){var z="&dvp_strhd="+v.duration;z+="&dvpx_strhd="+v.duration}v&&v.url||(v=V(e));v&&v.url&&(r="&aUrl="+encodeURIComponent(v.url),C="&aUrlD="+v.depth);var x=e.depth+d;l&&e.depth--}catch(H){z=C=r=x=e.depth=""}a:{try{if("object"==typeof window.$ovv||"object"==typeof window.parent.$ovv){var t=1;break a}}catch(H){}t=0}d=function(){function b(d){c++;var e=d.parent==d;return d.mraid||e?d.mraid:20>=c&&b(d.parent)}var d=window._dv_win||window,c=0;try{return b(d)}catch(fa){}}();
var k=c.script.src;t="&ctx="+(dv_GetParam(k,"ctx")||"")+"&cmp="+(dv_GetParam(k,"cmp")||"")+"&plc="+(dv_GetParam(k,"plc")||"")+"&sid="+(dv_GetParam(k,"sid")||"")+"&advid="+(dv_GetParam(k,"advid")||"")+"&adsrv="+(dv_GetParam(k,"adsrv")||"")+"&unit="+(dv_GetParam(k,"unit")||"")+"&isdvvid="+(dv_GetParam(k,"isdvvid")||"")+"&uid="+c.uid+"&tagtype="+(dv_GetParam(k,"tagtype")||"")+"&adID="+(dv_GetParam(k,"adID")||"")+"&app="+(dv_GetParam(k,"app")||"")+"&sup="+(dv_GetParam(k,"sup")||"")+"&isovv="+t+"&gmnpo="+
(dv_GetParam(k,"gmnpo")||"")+"&crt="+(dv_GetParam(k,"crt")||"");"1"==dv_GetParam(k,"foie")&&(t+="&foie=1");d&&(t+="&ismraid=1");(d=dv_GetParam(k,"xff"))&&(t+="&xff="+d);(d=dv_GetParam(k,"vssd"))&&(t+="&vssd="+d);(d=dv_GetParam(k,"apifw"))&&(t+="&apifw="+d);(d=dv_GetParam(k,"vstvr"))&&(t+="&vstvr="+d);(d=dv_GetParam(k,"tvcp"))&&(t+="&tvcp="+d);n&&(t+="&urlsrc=sf");y&&(t+="&sfe=1");navigator&&navigator.maxTouchPoints&&5==navigator.maxTouchPoints&&(t+="&touch=1");navigator&&navigator.platform&&(t+="&nav_pltfrm="+
navigator.platform);z&&(t+=z);p&&(t+="&useragent="+p);m&&(t+="&brid="+m.ID+"&brver="+m.version+"&bridua="+m.ID_UA);t+="&dup="+dv_GetParam(k,"dup");try{t+=dv_AppendIQPAParams(k)}catch(H){}(n=dv_GetParam(k,"turl"))&&(t+="&turl="+n);(n=dv_GetParam(k,"tagformat"))&&(t+="&tagformat="+n);"video"===dv_GetParam(k,"tagtype")&&(t+="&DVP_BYPASS219=1");t+=W();q=q?"&dvf=0":"";n=M("maple")?"&dvf=1":"";g=(window._dv_win.dv_config.verifyJSURL||"https://"+(window._dv_win.dv_config.bsAddress||"rtb"+c.dvregion+".doubleverify.com")+
"/verify.js")+"?flvr=0&jsCallback="+c.callbackName+"&jsTagObjCallback="+c.tagObjectCallbackName+"&num=6"+t+"&srcurlD="+e.depth+"&ssl="+c.ssl+q+n+"&refD="+x+c.tagIntegrityFlag+c.tagHasPassbackFlag+"&htmlmsging="+(g?"1":"0")+"&tstype="+J(window._dv_win);(x=dv_GetDynamicParams(k,"dvp").join("&"))&&(g+="&"+x);(x=dv_GetDynamicParams(k,"dvpx").join("&"))&&(g+="&"+x);if(!1===h||u)g=g+("&dvp_isBodyExistOnLoad="+(h?"1":"0"))+("&dvp_isOnHead="+(u?"1":"0"));f="srcurl="+encodeURIComponent(f);(h=X())&&(f+="&ancChain="+
encodeURIComponent(h));(e=Y(e))&&(f+="&canurl"+encodeURIComponent(e));e=4E3;/MSIE (\d+\.\d+);/.test(navigator.userAgent)&&7>=new Number(RegExp.$1)&&(e=2E3);if(h=dv_GetParam(k,"referrer"))h="&referrer="+h,g.length+h.length<=e&&(g+=h);(h=dv_GetParam(k,"prr"))&&(g+="&prr="+h);(h=dv_GetParam(k,"iframe"))&&(g+="&iframe="+h);(h=dv_GetParam(k,"gdpr"))&&(g+="&gdpr="+h);(h=dv_GetParam(k,"gdpr_consent"))&&(g+="&gdpr_consent="+h);r.length+C.length+g.length<=e&&(g+=C,f+=r);(r=Z())&&(g+="&m1="+r);(r=aa())&&0<
r.f&&(g+="&bsig="+r.f,g+="&usig="+r.s);r=ba();0<r&&(g+="&hdsig="+r);navigator&&navigator.hardwareConcurrency&&(g+="&noc="+navigator.hardwareConcurrency);g+=ca();r=da();g+="&vavbkt="+r.vdcd;g+="&lvvn="+r.vdcv;""!=r.err&&(g+="&dvp_idcerr="+encodeURIComponent(r.err));"prerender"===window._dv_win.document.visibilityState&&(g+="&prndr=1");(k=dv_GetParam(k,"wrapperurl"))&&1E3>=k.length&&g.length+k.length<=e&&(g+="&wrapperurl="+k);g+="&"+b.getVersionParamName()+"="+b.getVersion();b="&eparams="+encodeURIComponent(D(f));
g=g.length+b.length<=e?g+b:g+"&dvf=3";window.performance&&window.performance.mark&&window.performance.measure&&window.performance.getEntriesByName&&(window.performance.mark("dv_create_req_end"),window.performance.measure("dv_creqte_req","dv_create_req_start","dv_create_req_end"),(b=window.performance.getEntriesByName("dv_creqte_req"))&&0<b.length&&(g+="&dvp_exetime="+b[0].duration.toFixed(2)));for(var w in c)c.hasOwnProperty(w)&&void 0!==c[w]&&-1<["number","string"].indexOf(typeof c[w])&&-1===["protocol",
"callbackName","dvregion"].indexOf(w.toLowerCase())&&!w.match(/^tag[A-Z]/)&&!(new RegExp("(\\?|&)"+w+"=","gi")).test(g)&&(g+=["&",w,"=",encodeURIComponent(c[w])].join(""));return{isSev1:!1,url:g}}function W(){var b="";try{var c=window._dv_win.parent;b+="&chro="+(void 0===c.chrome?"0":"1");b+="&hist="+(c.history?c.history.length:"");b+="&winh="+c.innerHeight;b+="&winw="+c.innerWidth;b+="&wouh="+c.outerHeight;b+="&wouw="+c.outerWidth;c.screen&&(b+="&scah="+c.screen.availHeight,b+="&scaw="+c.screen.availWidth)}catch(f){}return b}
function da(){var b=[],c=function(b){e(b,null!=b.AZSD,9);e(b,b.location.hostname!=b.encodeURIComponent(b.location.hostname),10);e(b,null!=b.cascadeWindowInfo,11);e(b,null!=b._rvz,32);e(b,null!=b.FO_DOMAIN,34);e(b,null!=b.va_subid,36);e(b,b._GPL&&b._GPL.baseCDN,40);e(b,f(b,"__twb__")&&f(b,"__twb_cb_"),43);e(b,null!=b.landingUrl&&null!=b.seList&&null!=b.parkingPPCTitleElements&&null!=b.allocation,45);e(b,f(b,"_rvz",function(b){return null!=b.publisher_subid}),46);e(b,null!=b.cacildsFunc&&null!=b.n_storesFromFs,
47);e(b,b._pcg&&b._pcg.GN_UniqueId,54);e(b,f(b,"__ad_rns_")&&f(b,"_$_"),64);e(b,null!=b.APP_LABEL_NAME_FULL_UC,71);e(b,null!=b._priam_adblock,81);e(b,b.supp_ads_host&&b.supp_ads_host_overridden,82);e(b,b.uti_xdmsg_manager&&b.uti_xdmsg_manager.cb,87);e(b,b.LogBundleData&&b.addIframe,91);e(b,b.xAdsXMLHelperId||b.xYKAffSubIdTag,95);e(b,b.__pmetag&&b.__pmetag.uid,98);e(b,b.CustomWLAdServer&&/(n\d{1,4}adserv)|(1ads|cccpmo|epommarket|epmads|adshost1)/.test(b.supp_ads_host_overridden),100)},f=function(b,
c,e){for(var d in b)if(-1<d.indexOf(c)&&(!e||e(b[d])))return!0;return!1},e=function(c,e,f){e&&-1==b.indexOf(f)&&b.push((c==window.top?-1:1)*f)};try{return function(){for(var b=window,e=0;10>e&&(c(b),b!=window.top);e++)try{b.parent.document&&(b=b.parent)}catch(g){break}}(),{vdcv:28,vdcd:b.join(","),err:void 0}}catch(d){return{vdcv:28,vdcd:"-999",err:d.message||"unknown"}}}function T(b){for(var c=0;10>c&&b!=window._dv_win.top;)c++,b=b.parent;return c}function J(b){if(b==window._dv_win.top)return $dvbs.Enums.TrafficScenario.OnPage;
try{for(var c=0;window._dv_win.top!=b&&10>=c;){var f=b.parent;if(!f.document)break;b=f;c++}}catch(e){}return b==window._dv_win.top?$dvbs.Enums.TrafficScenario.SameDomain:$dvbs.Enums.TrafficScenario.CrossDomain}function U(b,c,f){try{if(f.ID==$dvbs.Enums.BrowserId.IE||J(b)!=$dvbs.Enums.TrafficScenario.CrossDomain)return null;b.performance&&b.performance.mark&&b.performance.mark("dv_str_html_start");if(c){var e=c.toString().match(/^(?:https?:\/\/)?[\w\-\.]+\/[a-zA-Z0-9]/gi);if(e&&0<e.length)return null}var d=
b.document;if(d&&d.referrer){var l=d.referrer.replace(/\//g,"\\/").replace(/\./g,"\\."),g=new RegExp('(?:w{0,4}=")?'+l+"[^&\"; %,'\\$\\\\\\|]+","gi");c=/banner|adprefs|safeframe|sandbox|sf\.html/gi;f=/^\w{0,4}="/gi;var h=K(d,"script","src",g,c,f);if(!h){var u=d.referrer;e="";var q=d.getElementsByTagName("script");if(q)for(l=0;!e&&l<q.length;){var n=q[l].innerHTML;if(n&&-1!=n.indexOf(u)){var y=n.match(g);e=L(y,c,f)}l++}(h=e)||(h=K(d,"a","href",g,c,f))}d=htmlUrl=h;a:{if(b.performance&&b.performance.mark&&
b.performance.measure&&b.performance.getEntriesByName){b.performance.mark("dv_str_html_end");b.performance.measure("dv_str_html","dv_str_html_start","dv_str_html_end");var p=b.performance.getEntriesByName("dv_str_html");if(p&&0<p.length){var m=p[0].duration.toFixed(2);break a}}m=null}return{url:d,depth:-1,duration:m}}}catch(r){}return null}function L(b,c,f){var e="";if(b&&0<b.length)for(var d=0;d<b.length;d++){var l=b[d];l.length>e.length&&null==l.match(c)&&0!=l.indexOf('src="')&&0!=l.indexOf('turl="')&&
(e=l.replace(f,""))}return e}function K(b,c,f,e,d,l){b=b.querySelectorAll(c+"["+f+'*="'+b.referrer+'"]');var g="";if(b)for(c=0;!g&&c<b.length;)g=b[c][f].match(e),g=L(g,d,l),c++;return g}function V(b){try{if(1>=b.depth)return{url:"",depth:""};var c=[];c.push({win:window._dv_win.top,depth:0});for(var f,e=1,d=0;0<e&&100>d;){try{if(d++,f=c.shift(),e--,0<f.win.location.toString().length&&f.win!=b)return 0==f.win.document.referrer.length||0==f.depth?{url:f.win.location,depth:f.depth}:{url:f.win.document.referrer,
depth:f.depth-1}}catch(h){}var l=f.win.frames.length;for(var g=0;g<l;g++)c.push({win:f.win.frames[g],depth:f.depth+1}),e++}return{url:"",depth:""}}catch(h){return{url:"",depth:""}}}function X(){var b=window._dv_win[D("=@42E:@?")][D("2?46DE@C~C:8:?D")];if(b&&0<b.length){var c=[];c[0]=window._dv_win.location.protocol+"//"+window._dv_win.location.hostname;for(var f=0;f<b.length;f++)c[f+1]=b[f];return c.reverse().join(",")}return null}function Y(b){return(b=b.document.querySelector("link[rel=canonical]"))?
b.href:null}function D(b){new String;var c=new String,f;for(f=0;f<b.length;f++){var e=b.charAt(f);var d="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~".indexOf(e);0<=d&&(e="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~".charAt((d+47)%94));c+=e}return c}function E(){return Math.floor(1E12*(Math.random()+""))}function S(b){for(var c=[{id:4,brRegex:"OPR|Opera",verRegex:"(OPR/|Version/)"},{id:1,brRegex:"MSIE|Trident/7.*rv:11|rv:11.*Trident/7|Edge/|Edg/",
verRegex:"(MSIE |rv:| Edge/|Edg/)"},{id:2,brRegex:"Firefox",verRegex:"Firefox/"},{id:0,brRegex:"Mozilla.*Android.*AppleWebKit(?!.*Chrome.*)|Linux.*Android.*AppleWebKit.* Version/.*Chrome",verRegex:null},{id:0,brRegex:"AOL/.*AOLBuild/|AOLBuild/.*AOL/|Puffin|Maxthon|Valve|Silk|PLAYSTATION|PlayStation|Nintendo|wOSBrowser",verRegex:null},{id:3,brRegex:"Chrome",verRegex:"Chrome/"},{id:5,brRegex:"Safari|(OS |OS X )[0-9].*AppleWebKit",verRegex:"Version/"}],f=0,e="",d=0;d<c.length;d++)if(null!=b.match(new RegExp(c[d].brRegex))){f=
c[d].id;if(null==c[d].verRegex)break;b=b.match(new RegExp(c[d].verRegex+"[0-9]*"));null!=b&&(e=b[0].match(new RegExp(c[d].verRegex)),e=b[0].replace(e[0],""));break}c=ea();4==f&&(c=f);return{ID:c,version:c===f?e:"",ID_UA:f}}function ea(){try{if(null!=window._phantom||null!=window.callPhantom)return 99;if(document.documentElement.hasAttribute&&document.documentElement.hasAttribute("webdriver")||null!=window.domAutomation||null!=window.domAutomationController||null!=window._WEBDRIVER_ELEM_CACHE)return 98;
if(void 0!=window.opera&&void 0!=window.history.navigationMode||void 0!=window.opr&&void 0!=window.opr.addons&&"function"==typeof window.opr.addons.installExtension)return 4;if(void 0!=document.uniqueID&&"string"==typeof document.uniqueID&&(void 0!=document.documentMode&&0<=document.documentMode||void 0!=document.all&&"object"==typeof document.all||void 0!=window.ActiveXObject&&"function"==typeof window.ActiveXObject)||window.document&&window.document.updateSettings&&"function"==typeof window.document.updateSettings||
Object.values&&navigator&&Object.values(navigator.plugins).some(function(b){return-1!=b.name.indexOf("Edge PDF")}))return 1;if(void 0!=window.chrome&&"function"==typeof window.chrome.csi&&"function"==typeof window.chrome.loadTimes&&void 0!=document.webkitHidden&&(1==document.webkitHidden||0==document.webkitHidden))return 3;if(void 0!=window.mozInnerScreenY&&"number"==typeof window.mozInnerScreenY&&void 0!=window.mozPaintCount&&0<=window.mozPaintCount&&void 0!=window.InstallTrigger&&void 0!=window.InstallTrigger.install)return 2;
var b=!1;try{var c=document.createElement("p");c.innerText=".";c.style="text-shadow: rgb(99, 116, 171) 20px -12px 2px";b=void 0!=c.style.textShadow}catch(f){}return(0<Object.prototype.toString.call(window.HTMLElement).indexOf("Constructor")||window.webkitAudioPannerNode&&window.webkitConvertPointFromNodeToPage)&&b&&void 0!=window.innerWidth&&void 0!=window.innerHeight?5:0}catch(f){return 0}}function Z(){try{var b=0,c=function(c,d){d&&32>c&&(b=(b|1<<c)>>>0)},f=function(b,c){return function(){return b.apply(c,
arguments)}},e="svg"===document.documentElement.nodeName.toLowerCase(),d=function(){return"function"!==typeof document.createElement?document.createElement(arguments[0]):e?document.createElementNS.call(document,"http://www.w3.org/2000/svg",arguments[0]):document.createElement.apply(document,arguments)},l=["Moz","O","ms","Webkit"],g=["moz","o","ms","webkit"],h={style:d("modernizr").style},u=function(b,c){function e(){g&&(delete h.style,delete h.modElem)}var f;for(f=["modernizr","tspan","samp"];!h.style&&
f.length;){var g=!0;h.modElem=d(f.shift());h.style=h.modElem.style}var n=b.length;for(f=0;f<n;f++){var l=b[f];~(""+l).indexOf("-")&&(l=cssToDOM(l));if(void 0!==h.style[l])return e(),"pfx"==c?l:!0}e();return!1},q=function(b,c,d){var e=b.charAt(0).toUpperCase()+b.slice(1),h=(b+" "+l.join(e+" ")+e).split(" ");if("string"===typeof c||"undefined"===typeof c)return u(h,c);h=(b+" "+g.join(e+" ")+e).split(" ");for(var n in h)if(h[n]in c){if(!1===d)return h[n];b=c[h[n]];return"function"===typeof b?f(b,d||
c):b}return!1};c(0,!0);c(1,q("requestFileSystem",window));c(2,window.CSS?"function"==typeof window.CSS.escape:!1);c(3,q("shapeOutside","content-box",!0));return b}catch(n){return 0}}function F(){var b=window,c=0;try{for(;b.parent&&b!=b.parent&&b.parent.document&&!(b=b.parent,10<c++););}catch(f){}return b}function aa(){try{var b=F(),c=0,f=0,e=function(b,d,e){e&&(c+=Math.pow(2,b),f+=Math.pow(2,d))},d=b.document;e(14,0,b.playerInstance&&d.querySelector('script[src*="ads-player.com"]'));e(14,1,(b.CustomWLAdServer||
b.DbcbdConfig)&&(a=d.querySelector('p[class="footerCopyright"]'),a&&a.textContent.match(/ MangaLife 2016/)));e(15,2,b.zpz&&b.zpz.createPlayer);e(15,3,b.vdApp&&b.vdApp.createPlayer);e(15,4,d.querySelector('body>div[class="z-z-z"]'));e(16,5,b.xy_checksum&&b.place_player&&(b.logjwonready&&b.logContentPauseRequested||b.jwplayer));e(17,6,b==b.top&&""==d.title?(a=d.querySelector('body>object[id="player"]'),a&&a.data&&1<a.data.indexOf("jwplayer")&&"visibility: visible;"==a.getAttribute("style")):!1);e(17,
7,d.querySelector('script[src*="sitewebvideo.com"]'));e(17,8,b.InitPage&&b.cef&&b.InitAd);e(17,9,b==b.top&&""==d.title?(a=d.querySelector("body>#player"),null!=a&&null!=(null!=a.querySelector('div[id*="opti-ad"]')||a.querySelector('iframe[src="about:blank"]'))):!1);e(17,10,b==b.top&&""==d.title&&b.InitAdPlayer?(a=d.querySelector('body>div[id="kt_player"]'),null!=a&&null!=a.querySelector('div[class="flash-blocker"]')):!1);e(17,11,null!=b.clickplayer&&null!=b.checkRdy2);e(19,12,b.instance&&b.inject&&
d.querySelector('path[id="cp-search-0"]'));e(20,13,function(){try{if(b.top==b&&0<b.document.getElementsByClassName("asu").length)for(var c=b.document.styleSheets,d=0;d<c.length;d++)for(var e=b.document.styleSheets[d].cssRules,f=0;f<e.length;f++)if("div.kk"==e[f].selectorText||"div.asu"==e[f].selectorText)return!0}catch(r){}}());a:{try{var l=null!=d.querySelector('div[id="kt_player"][hiegth]');break a}catch(n){}l=void 0}e(21,14,l);a:{try{var g=b.top==b&&null!=b.document.querySelector('div[id="asu"][class="kk"]');
break a}catch(n){}g=void 0}e(22,15,g);a:{try{var h=d.querySelector('object[data*="/VPAIDFlash.swf"]')&&d.querySelector('object[id*="vpaid_video_flash_tester_el"]')&&d.querySelector('div[id*="desktopSubModal"]');break a}catch(n){}h=void 0}e(25,16,h);var u=navigator.userAgent;if(u&&-1<u.indexOf("Android")&&-1<u.indexOf(" wv)")&&b==window.top){var q=d.querySelector('img[src*="dealsneartome.com"]')||(b.__cads__?!0:!1)||0<d.querySelectorAll('img[src*="/tracker?tag="]').length;e(28,17,q||!1)}return{f:c,
s:f}}catch(n){return null}}function ba(){try{var b=F(),c=0,f=b.document;b==window.top&&""==f.title&&!f.querySelector("meta[charset]")&&f.querySelector('div[style*="background-image: url("]')&&(f.querySelector('script[src*="j.pubcdn.net"]')||f.querySelector('span[class="ad-close"]'))&&(c+=Math.pow(2,6));return c}catch(e){return null}}function ca(){try{var b="&fcifrms="+window.top.length;window.history&&(b+="&brh="+window.history.length);var c=F(),f=c.document;if(c==window.top){b+="&fwc="+((c.FB?1:
0)+(c.twttr?2:0)+(c.outbrain?4:0)+(c._taboola?8:0));try{f.cookie&&(b+="&fcl="+f.cookie.length)}catch(e){}c.performance&&c.performance.timing&&0<c.performance.timing.domainLookupStart&&0<c.performance.timing.domainLookupEnd&&(b+="&flt="+(c.performance.timing.domainLookupEnd-c.performance.timing.domainLookupStart));f.querySelectorAll&&(b+="&fec="+f.querySelectorAll("*").length)}return b}catch(e){return""}}var B=this,A=function(){function b(b,c){var f=[];c&&l.forEach(function(b){var d=dv_GetParam(c,
b);""!==d&&null!==d&&f.push(["dvp_"+b,d].join("="))});var g=window&&window._dv_win||{};g=g.dv_config=g.dv_config||{};g=dv_getDVBSErrAddress(g);var n=[d,e].join("="),q=["dvp_cert",h[b]].join("=");b=["dvp_jsErrMsg",b].join("=");g+=["/verify.js?flvr=0&ctx=818052&cmp=1619415&dvp_isLostImp=1&ssl=1",n,q,b,f.join("&")].join("&");(new Image(1,1)).src="https://"+g}function c(c,d){var e=window._dv_win.dv_config.bs_renderingMethod||function(b){document.write(b)};d="AdRenderedUponVerifyFailure__"+(d||"");if(B&&
B.tagParamsObj&&B.tagParamsObj.tagAdtag)try{e(B.tagParamsObj.tagAdtag)}catch(p){d+="__RenderingMethodFailed"}else B?B.tagParamsObj?B.tagParamsObj.tagAdtag||(d+="__HandlerTagParamsObjTagAdtag__Undefined"):d+="__HandlerTagParamsObj__Undefined":d+="__Handler__Undefined";b(d,c)}var f=!1,e,d,l=["ctx","cmp","plc","sid"],g=[B.constructor&&B.constructor.name||"UKDV","__",E()].join(""),h={VerifyLoadJSONPCallbackFailed:1,VerifyFailedToLoad:2},u={onResponse:function(d){f||(b("VerifyCallbackFailed",d),c(d,"VCF"))},
onError:function(d){b("VerifyFailedToLoad",d);c(d,"VFTL")}};u.reportError=b;u.isJSONPCalled=f;window._dv_win[g]={globalScopeVerifyErrorHandler:u};return{setVersionData:function(b,c){d=b;e=c},setIsJSONPCalled:function(b){f=b},getIsJSONPCalled:function(){return f},onLoad:dv_onResponse,onError:dv_onError,uniqueKey:g}}();this.createRequest=function(){window.performance&&window.performance.mark&&window.performance.mark("dv_create_req_start");var b=!1,c=window._dv_win,f=0,e=!1,d;try{for(d=0;10>=d;d++)if(null!=
c.parent&&c.parent!=c)if(0<c.parent.location.toString().length)c=c.parent,f++,b=!0;else{b=!1;break}else{0==d&&(b=!0);break}}catch(r){b=!1}a:{try{var l=c.$sf;break a}catch(r){}l=void 0}var g=(d=c.location&&c.location.ancestorOrigins)&&d[d.length-1];if(0==c.document.referrer.length)b=c.location;else if(b)b=c.location;else{b=c.document.referrer;a:{try{var h=c.$sf&&c.$sf.ext&&c.$sf.ext.hostURL&&c.$sf.ext.hostURL();break a}catch(r){}h=void 0}if(h&&(!d||0==h.indexOf(g))){b=h;var u=!0}e=!0}if(!window._dv_win.dvbsScriptsInternal||
!window._dv_win.dvbsProcessed||0==window._dv_win.dvbsScriptsInternal.length)return{isSev1:!1,url:null};d=window._dv_win.dv_config&&window._dv_win.dv_config.isUT?window._dv_win.dvbsScriptsInternal[window._dv_win.dvbsScriptsInternal.length-1]:window._dv_win.dvbsScriptsInternal.pop();h=d.script;this.dv_script_obj=d;this.dv_script=h;window._dv_win.dvbsProcessed.push(d);window._dv_win._dvScripts.push(h);g=h.src;this.dvOther=0;this.dvStep=1;var q=window._dv_win.dv_config?window._dv_win.dv_config.dv_GetRnd?
window._dv_win.dv_config.dv_GetRnd():E():E();d=window.parent.postMessage&&window.JSON;var n={};try{for(var y=/[\?&]([^&]*)=([^&#]*)/gi,p=y.exec(g);null!=p;)"eparams"!==p[1]&&(n[p[1]]=p[2]),p=y.exec(g);var m=n}catch(r){m=n}this.tagParamsObj=m;m.perf=this.perf;m.uid=q;m.script=this.dv_script;m.callbackName="__verify_callback_"+m.uid;m.tagObjectCallbackName="__tagObject_callback_"+m.uid;m.tagAdtag=null;m.tagPassback=null;m.tagIntegrityFlag="";m.tagHasPassbackFlag="";0==(null!=m.tagformat&&"2"==m.tagformat)&&
(p=R(m.script),m.tagAdtag=p.tagAdTag,m.tagPassback=p.tagPassback,p.isBadImp?m.tagIntegrityFlag="&isbadimp=1":p.hasPassback&&(m.tagHasPassbackFlag="&tagpb=1"));p=(/iPhone|iPad|iPod|\(Apple TV|iOS|Coremedia|CFNetwork\/.*Darwin/i.test(navigator.userAgent)||navigator.vendor&&"apple, inc."===navigator.vendor.toLowerCase())&&!window.MSStream;m.protocol="https:";m.ssl="1";g=m;(q=window._dv_win.dvRecoveryObj)?("2"!=g.tagformat&&(q=q[g.ctx]?q[g.ctx].RecoveryTagID:q._fallback_?q._fallback_.RecoveryTagID:1,
1===q&&g.tagAdtag?document.write(g.tagAdtag):2===q&&g.tagPassback&&document.write(g.tagPassback)),g=!0):g=!1;if(g)return{isSev1:!0};this.dvStep=2;Q(m);h=h&&h.parentElement&&h.parentElement.tagName&&"HEAD"===h.parentElement.tagName;this.dvStep=3;return I(this,m,b,c,f,e,d,!0,h,p,u,l)};this.sendRequest=function(b){var c=dv_GetParam(b,"tagformat");if(A)try{A.setVersionData(this.getVersionParamName(),this.getVersion()),c&&"2"==c?$dvbs.domUtilities.addScriptResource(b,document.body,A.onLoad,A.onError,A.uniqueKey):
dv_sendScriptRequest(b,A.onLoad,A.onError,A.uniqueKey)}catch(f){c&&"2"==c?$dvbs.domUtilities.addScriptResource(b,document.body):dv_sendScriptRequest(b)}else c&&"2"==c?$dvbs.domUtilities.addScriptResource(b,document.body):dv_sendScriptRequest(b);return!0};this.isApplicable=function(){return!0};this.onFailure=function(){};window.debugScript&&(window.CreateUrl=I);this.getVersionParamName=function(){return"ver"};this.getVersion=function(){return"165"}};


function dvbs_src_main(dvbs_baseHandlerIns, dvbs_handlersDefs) {

    this.bs_baseHandlerIns = dvbs_baseHandlerIns;
    this.bs_handlersDefs = dvbs_handlersDefs;

    this.exec = function () {
        try {
            window._dv_win = (window._dv_win || window);
            window._dv_win.$dvbs = (window._dv_win.$dvbs || new dvBsType());

            window._dv_win.dv_config = window._dv_win.dv_config || {};
            window._dv_win.dv_config.bsErrAddress = window._dv_win.dv_config.bsAddress || 'rtb0.doubleverify.com';

            var errorsArr = (new dv_rolloutManager(this.bs_handlersDefs, this.bs_baseHandlerIns)).handle();
            if (errorsArr && errorsArr.length > 0)
                dv_SendErrorImp(window._dv_win.dv_config.bsErrAddress + '/verify.js?flvr=0&ctx=818052&cmp=1619415&num=6', errorsArr);
        }
        catch (e) {
            try {
                dv_SendErrorImp(window._dv_win.dv_config.bsErrAddress + '/verify.js?flvr=0&ctx=818052&cmp=1619415&num=6&dvp_isLostImp=1', {dvp_jsErrMsg: encodeURIComponent(e)});
            } catch (e) {
            }
        }
    };
};


try {
    window._dv_win = window._dv_win || window;
    var dv_baseHandlerIns = new dv_baseHandler();
	

    var dv_handlersDefs = [];
    (new dvbs_src_main(dv_baseHandlerIns, dv_handlersDefs)).exec();
} catch (e) { }
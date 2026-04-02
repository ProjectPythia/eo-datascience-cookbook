import {
  __commonJS
} from "/eo-datascience-cookbook/build/_shared/chunk-CGOEG7L2.js";

// ../../node_modules/highlight.js/lib/languages/vbscript-html.js
var require_vbscript_html = __commonJS({
  "../../node_modules/highlight.js/lib/languages/vbscript-html.js"(exports, module) {
    function vbscriptHtml(hljs) {
      return {
        name: "VBScript in HTML",
        subLanguage: "xml",
        contains: [
          {
            begin: "<%",
            end: "%>",
            subLanguage: "vbscript"
          }
        ]
      };
    }
    module.exports = vbscriptHtml;
  }
});
export default require_vbscript_html();
//# sourceMappingURL=/eo-datascience-cookbook/build/_shared/vbscript-html-XLLGZQMF.js.map

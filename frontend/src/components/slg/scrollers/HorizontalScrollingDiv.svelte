<script>
//   $(document).ready(function() {
//     $("#text-container").on("scroll", onScroll);
//   });

//   function onScroll(e) {
//     elem = e.currentTarget;
//     perc = percScrolled(elem);
//     arrowElem = $("#arrow");

//     setPercOpacity(elem, (1 - perc).toString(), "box-shadow");
//     setPercOpacity(arrowElem[0], (1 - perc).toString());

//     setPercPosition({
//       jQueryElem: arrowElem,
//       range: [75, 85],
//       type: "%",
//       attr: "top",
//       perc: perc
//     });
//   }

//   function setPercPosition(obj = {}) {
//     let max = obj.range[1] - obj.range[0];
//     obj.jQueryElem.css(
//       obj.attr,
//       (obj.range[0] + obj.perc * max).toString() + obj.type
//     );
//   }

//   function hideArrow() {}

//   function toggleBoxShadow() {}

//   function percScrolled(elem) {
//     var $elem = $(elem);
//     return $elem.scrollTop() / (elem.scrollHeight - $elem.outerHeight());
//   }

//   function setPercOpacity(elem, percOpacity, attr = null) {
//     // percentages passed as 0 to 1 value
//     if (attr) {
//       let style = window.getComputedStyle(elem)[attr];
//       let color = style;
//       let restOfstring = null;
//       if (attr == "box-shadow") {
//         color, (restOfString = separateBoxShadow(style));
//       }
//       color = setColorOpacity(color, percOpacity);

//       if (restOfString) {
//         elem.style.setProperty(attr, color + restOfString);
//       } else {
//         elem.style.setProperty(attr, color);
//       }
//     } else {
//       elem.style.opacity = percOpacity;
//     }
//   }

//   function setColorOpacity(color, opacity) {
//     components = /rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*\d+[\.\d+]*)*\)/g.exec(
//       color
//     );
//     return `rgba(${components[1]}, ${components[2]}, ${components[3]}, ${opacity})`;
//   }

//   function separateBoxShadow(style) {
//     let color = /rgba?\(.*?\)/g.exec(style);
//     let restOfString = style.slice(color.toString().length);
//     return color, restOfString;
//   }
</script>

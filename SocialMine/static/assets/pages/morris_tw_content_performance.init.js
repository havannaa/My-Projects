!function(e) {
    "use strict";
    var a=function() {}
    ;
    a.prototype.createBarChart=function(e, a, r, t, i, o) {
        Morris.Bar( {
            element: e, data: a, xkey: r, ykeys: t, labels: i, gridLineColor: "#eef0f2", barSizeRatio: .4, resize: !0, hideHover: "auto", barColors: o
        }
        )
    }
    ,
    a.prototype.createDonutChart=function(e, a, r) {
        Morris.Donut( {
            element: e, data: a, resize: !0, colors: r
        }
        )
    }
    ,
    a.prototype.init=function() {
        this.createBarChart("morris-bar-example", [ {
            y: "21", a: 100, b: 90
        }
        , {
            y: "22", a: 75, b: 65
        }
        , {
            y: "23", a: 50, b: 40
        }
        , {
            y: "24", a: 75, b: 65
        }
        , {
            y: "25", a: 50, b: 40
        }
        , {
            y: "26", a: 75, b: 65
        }
        , {
            y: "27", a: 100, b: 90
        }
        , {
            y: "28", a: 90, b: 75
        }
        ], "y", ["a", "b"], ["Video", "Text"], ["#5b6be8", "#0097a7"]);
		
        this.createDonutChart("morris-donut-example", [ {
            label: "Video", value: 75
        }
        , {
            label: "Text", value: 25
        }
        ], ["#ffbb44", "#0097a7"])
    }
    ,
    e.MorrisCharts=new a,
    e.MorrisCharts.Constructor=a
}

(window.jQuery),
function(e) {
    "use strict";
    window.jQuery.MorrisCharts.init()
}

();
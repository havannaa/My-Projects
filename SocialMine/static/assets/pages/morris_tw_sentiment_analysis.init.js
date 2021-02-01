!function(e) {
    "use strict";
    var a=function() {}
    ;
    a.prototype.createLineChart=function(e, a, r, t, i, o) {
        Morris.Line( {
            element: e, data: a, xkey: r, ykeys: t, labels: i, hideHover: "auto", gridLineColor: "#eef0f2", resize: !0, lineColors: o
        }
        )
    }
    ,
    a.prototype.createAreaChart=function(e, a, r, t, i, o, s, b) {
        Morris.Area( {
            element: e, pointSize: 3, lineWidth: 2, data: t, xkey: i, ykeys: o, labels: s, resize: !0, hideHover: "auto", gridLineColor: "#eef0f2", lineColors: b
        }
        )
    }
    ,
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
        this.createLineChart("morris-line-example", [ {
            y: "2009", a: 100, b: 90
        }
        , {
            y: "2010", a: 75, b: 65
        }
        , {
            y: "2011", a: 50, b: 40
        }
        , {
            y: "2012", a: 75, b: 65
        }
        , {
            y: "2013", a: 50, b: 40
        }
        , {
            y: "2014", a: 75, b: 65
        }
        , {
            y: "2015", a: 100, b: 90
        }
        ], "y", ["a", "b"], ["Series A", "Series B"], ["#5b6be8", "#0097a7"]);
        this.createAreaChart("morris-area-example", 0, 0, [ {
            y: "2009", a: 10, b: 20
        }
        , {
            y: "2010", a: 75, b: 65
        }
        , {
            y: "2011", a: 50, b: 40
        }
        , {
            y: "2012", a: 75, b: 65
        }
        , {
            y: "2013", a: 50, b: 40
        }
        , {
            y: "2014", a: 75, b: 65
        }
        , {
            y: "2015", a: 90, b: 60
        }
        , {
            y: "2016", a: 90, b: 75
        }
        ], "y", ["a", "b"], ["Series A", "Series B"], ["#5b6be8", "#0097a7"]);
        this.createBarChart("morris-bar-example", [ {
            y: "2009", a: 100, b: 90
        }
        , {
            y: "2010", a: 75, b: 65
        }
        , {
            y: "2011", a: 50, b: 40
        }
        , {
            y: "2012", a: 75, b: 65
        }
        , {
            y: "2013", a: 50, b: 40
        }
        , {
            y: "2014", a: 75, b: 65
        }
        , {
            y: "2015", a: 100, b: 90
        }
        , {
            y: "2016", a: 90, b: 75
        }
        ], "y", ["a", "b"], ["Series A", "Series B"], ["#5b6be8", "#0097a7"]);
        this.createDonutChart("morris-donut-example", [ {
            label: "Download Sales", value: 12
        }
        , {
            label: "In-Store Sales", value: 30
        }
        , {
            label: "Mail-Order Sales", value: 20
        }
        ], ["#ffbb44", "#0097a7", "#67a8e4"])
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
var step;
var __s;

module("STEP Passage Criteria View Test", {
    setup: function () {
        step = {
            util : {ui : { autocompleteSearch : function() { } } },
            defaults : { passage : {
                interNamedOptions: ["A", "B", "C", "INTERLINEAR"],
                interOptions: ["x", "y", "z", "Interlinear"],
                interOptionsNoInterlinear : ["x", "y", "z"]}}
        },
        __s = { info_about_bible : "%1$s" };
        $.widget("custom.versions", { options : {}});
        $("<body>").append($("<div id='someId'>"));
    }
});

test("PassageCriteriaView Set if changed", function () {
    var model = new PassageModel;
    var view = new PassageCriteriaView({ model : model});

    var inputTest = { innerValue : "oldValue", val : function(newValue) {
        if(newValue) {
            ok(true, "Set was called")
            this.innerValue = newValue;
        }
        return this.innerValue;
    }};

    //we expect 1 setter + the equals at the end of this method
    expect(2);

    //we check that the new value always gets set
    view._setValIfChanged(inputTest, "newValue");
    view._setValIfChanged(inputTest, "newValue");

    equals("newValue", inputTest.val());
});


test("PassageCriteriaView Resync disables and sets the source correctly", function () {
    var model = new PassageModel;
    var view = new PassageCriteriaView({ model : model});

    view.interlinearMode = {
        prop : function(key, disabled) { this.disabledValue = disabled; },
        autocomplete : function(option, source, options) { this.optionsValue = options; },
        val : function(newValue) { this.value = newValue }
    };


    //we check that resyncing enables prop and sets the source
    var sampleOptions = ["x", "y"];
    model.getAvailableInterlinearOptions = function() { return sampleOptions };
    view._resyncAvailableInterlinearOption();
    equals(false, view.interlinearMode.disabledValue);
    equals(sampleOptions, view.interlinearMode.optionsValue);

    //if there are no sample options, then we need to make sure we have blanked and changed the source
    sampleOptions = [];
    view._resyncAvailableInterlinearOption();
    equals(true, view.interlinearMode.disabledValue);
    equals("", view.interlinearMode.value);
});

test("Tests that link and biblebooks get updated on version update", function() {
    var model = new PassageModel;

    //we need a link for this to work
    var link = $("<a>").prop("href", "something").addClass("infoAboutVersion");
    var el = $("<div>").append(link)

    var view = new PassageCriteriaView({ model : model, el : el});

    model.set("version", "ASV");
    model.trigger("change:version", {});

    //check text and link has changed
    ok(link.prop("href").indexOf("ASV") != -1);
    ok(link.prop("title").indexOf("ASV") != -1);
});


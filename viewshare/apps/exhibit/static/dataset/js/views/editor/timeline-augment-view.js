/*global define */
define([
    'handlebars',
    'jquery',
    'models/composite-property',
    'text!templates/timeline-augment.html'
], function (
    Handlebars,
    $,
    CompositePropertyModel,
    timelineAugmentTemplate
) {
    'use strict';
    /**
     * View that can add a CompositeModel to a RecordCollection. This prepares
     * the RecordCollection to be sent to an Akara server for augmentation.
     * @constructor
     * @param {object} options.propertyCollection - PropertyCollection
     * we're augmenting
     * @param {object} options.$el - container Element object for this view
     */
    var TimelineAugmentView = function(options) {
        this.initialize.apply(this, [options]);
    };

    $.extend(TimelineAugmentView.prototype, {
        initialize: function(options) {
            this.propertyCollection = options.propertyCollection;
            this.propertyOptions = options.propertyCollection.toOptions();
            this.$el = options.$el;
            this.newCompositeProperty = new CompositePropertyModel({
                id: undefined,
                label: undefined,
                type: 'date',
                value: [],
                augmentation: 'composite',
                composite: [],
                property_url: options.propertyCollection.propertiesURL
            });
            this.newCompositeProperty.Observer('augmentDataFailure')
                .subscribe(this.augmentDataFailureHandler.bind(this));
        },

        /** Compile the template we will use to render the View */
        template: Handlebars.compile(timelineAugmentTemplate),

        /** Event handler when a .name input is changed */
        changeNameHandler: function(event) {
            this.newCompositeProperty.label = event.target.value;
            this.newCompositeProperty.id(
                event.target.value.replace(' ', '_', 'g').toLowerCase());
        },

        /** Event handler when a .selcted input is clicked */
        changeCompositeHandler: function() {
            var i = 0;
            var selected = this.$el.find('.selected input:checked');
            var composites = [];
            for (i; i < selected.length; ++i) {
                composites.push(selected[i].value);
            }
            this.newCompositeProperty.composite = composites;
        },

        /**
         * Bubble up the 'augmentDataFailure' event from our
         * newCompositeProperty to anything that might be interested
         * (notificationView for example).
         */
        augmentDataFailureHandler: function(failure) {
            this.propertyCollection.publishAugmentDataFailure(failure);
        },

        render: function() {
            this.$el.html(this.template(this));
            this.$el.find('#new-timeline-property').on(
                'change', this.changeNameHandler.bind(this));
            this.$el.find('.selected input').on(
                'click', this.changeCompositeHandler.bind(this));
        },

        /** Remove event bindings, child views, and DOM elements */
        destroy: function() {
            this.$el.find('.name input').off(
                'change', this.changeNameHandler.bind(this));
            this.$el.find('.selected input').off(
                'click', this.changeCompositeHandler.bind(this));
            this.$el.remove();
        }
    });

    return TimelineAugmentView;
});

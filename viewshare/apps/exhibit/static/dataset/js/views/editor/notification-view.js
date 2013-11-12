/*global define */
define([
       'handlebars',
       'jquery',
       'text!templates/notification.html'
  ], function (
       Handlebars,
       $,
       notificationTemplate
  ) {
  'use strict';
  /**
   * View to display notifications. Any model that publishes an event that
   * should be picked up by the Notification view should include the
   * following data:
   * notificationLevel - 'info', 'warning', 'error', or 'success'
   * message - text displayed in the notification
   * lead (option) - bold type that appears at the beginning of the message
   * @constructor
   * @param {object} options.$el - container Element object for this view
   */
  var NotificationView = function(options) {
    this.initialize.apply(this, [options]);
  };

  $.extend(NotificationView.prototype, {
    initialize: function(options) {
      this.$el = options.$el;
    },

    /** Compile the template we will use to render the View */
    template: Handlebars.compile(notificationTemplate),

    /** Create a visual notification on a specified observable's event
     * @param {object} observable - Object that extends observer.js
     * @param {string} eventName - Name of the event NotificationView will handle
     * @return {func} notificationFunc - The function to be fired
     * on 'eventName'. This is used for removeSubscription.
     */
    addSubscription: function(observable, eventName, notificationLevel, message, lead) {
      var notificationFunc = this.addNotification.bind(
        this, notificationLevel, message, lead);
      observable.Observer(eventName).subscribe(notificationFunc);
      return notificationFunc;
    },

    /** Remove a notification subscription
     * @param {object} observable - Object that extends observer.js
     * @param {string} eventName - Name of the event NotificationView will handle
     * @param {func} notificationFunc - Function that was returned
     * from addSubscription
     */
    removeSubscription: function(observable, eventName, notificationFunc) {
      observable.Observer(eventName).unsubscribe(notificationFunc);
    },

    /**
     * Add a visual notification to the DOM
     * @param {string} notificationLevel - 'alert'|'info'|'error'
     * @param {string} message - text to display in notification
     * @param {string} lead - (optional) lead text to display in bold
     */
    addNotification: function(notificationLevel, message, lead) {
      var notification, status = 'alert';
      if (notificationLevel === 'info') {
        status = 'alert alert-info editor-notification';
      } else if (notificationLevel === 'error') {
        status = 'alert alert-error editor-notification';
      } else if (notificationLevel === 'success') {
        status = 'alert alert-success editor-notification';
      }
      notification = this.template({
        status: status,
        message: message,
        lead: lead
      });
      /* this.$el.prepend(notification); */

      this.$el.empty().append(notification);

      var editorAlert = this.$el.find(".editor-notification");

      window.setTimeout(function () {
	      editorAlert.fadeOut(2000, "linear",
	      function() { 
		  editorAlert.remove();
	      });
	  }, 4000);
      },

    /** Remove event bindings, child views, and DOM elements.
     * Views that call 'addSubscription' are responsible for
     * calling 'removeSubscription'.
     */
    destroy: function() {
      this.$el.empty();
    }
  });

  return NotificationView;
});

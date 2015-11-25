Parse.initialize("WqC4d6L2FC2qbgZbF2HjFYpERQOfl38DWpWiofGz", "jxn3V6WEv1J6I6Jn4Va5lOKeJLx3sQZEKslpGfHL");
var TestObject = Parse.Object.extend("TestObject");
var testObject = new TestObject();
testObject.save({foo: "bar"}).then(function(object) {
  alert("yay! it worked");
});

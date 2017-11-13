var app = angular.module('motty', ['ngResource', 'ngDialog'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// resources
app.factory('Actions', ['$resource', function($resource) {
    return $resource('/app/api/actions', null, {
        'get': {isArray:true}
    });
}]);
app.factory('Action', ['$resource', function($resource) {
    return $resource('/app/api/action/:actionId/:action', {actionId:'@id', action:'@action'}, {
        get: {method:'GET'},
        create: {method:'POST'},
        update: {method:'POST', action:'edit'},
        delete: {method:'GET', action:'delete'}
    });
}])

// controllers
app.controller('Tools.ctrl', function($scope, ngDialog) {
    $scope.openCreateForm = function(){
        ngDialog.open({ 
            template: '/static/templates/create-action-dialog.html', 
            controller: 'ActionCreate.ctrl'
        });
    };
});

app.controller('ActionCreate.ctrl', function($scope, $rootScope, Action){
    $scope.action = {name:"", url:"", method:"", contentType:"", body:""}
    $scope.save = function(){
        Action.create($scope.action, function(res){
            $rootScope.actions.push($scope.action);
            $scope.closeThisDialog();
        });
    };
});

app.controller('ActionList.ctrl', function($scope, $rootScope, Actions, Action){
    $rootScope.actions = [];

    Actions.get(function(res){
        $rootScope.actions = res;
    });
});
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
        delete: {method:'GET', action:'delete'},
        deleteAll: {method: 'POST', params: {actionId: 'delete', action: 'all'}}
    });
}])

// controllers
app.controller('Tools.ctrl', function($scope, $rootScope, ngDialog, Action) {
    $scope.openCreateForm = function(){
        ngDialog.open({ 
            template: '/static/templates/create-action-dialog.html', 
            controller: 'ActionCreate.ctrl'
        });
    };

    $scope.prepareToDelete = function(){
        $rootScope.is_deleting = true;
    };

    $scope.delete = function(){
        _ids = $rootScope.actions.filter(function(action){
            return action.isToDelete == true;
        }).map(function(action){
            return action.id;
        });

        if(_ids.length == 0) {
            $.notify('No selected actions.', { type: "warning" });
        } else {
            Action.deleteAll({ids:_ids}, function(res){
                $.notify('Successfully deleted.');

                $rootScope.actions = $rootScope.actions.filter(function(action){
                    return _ids.indexOf(action.id) == -1;
                });
                $rootScope.is_deleting = false;
            });
        }
    }

    $scope.cancel = function(){
        $rootScope.is_deleting = false;
        $rootScope.actions = $rootScope.actions.map(function(action){
            action.isToDelete = false;
            return action;
        })
    }
});

app.controller('ActionCreate.ctrl', function($scope, $rootScope, Action){
    $scope.action = {name:"", url:"", method:"", contentType:"application/json", body:""}
    $scope.save = function(){
        $.notify('Successfully created.');

        Action.create($scope.action, function(res){
            $rootScope.actions.push(res);
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
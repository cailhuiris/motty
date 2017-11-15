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
    return $resource('/app/api/action/:id/:action', {id:'@id', action:'@action'}, {
        get: {method:'GET'},
        create: {method:'POST'},
        update: {method:'POST', params: { action:'edit'} },
        delete: {method:'GET', params: {action:'delete'} },
        deleteAll: {method: 'POST', params: {id: 'delete', action: 'all'}}
    });
}])

app.run(function($rootScope, Actions){
    $rootScope.updateActions = function(){
        Actions.get(function(res){
            $rootScope.actions = res;
        });
    }
});

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

app.controller('ActionList.ctrl', function($scope, $rootScope, $timeout, Actions, Action, ngDialog){
    $rootScope.actions = [];

    Actions.get(function(res){
        $rootScope.actions = res;
    });

    $scope.showDetail = function($idx){
        var action = $rootScope.actions[$idx];
        Action.get({id: action.id}, function(res){
            $scope.action = res;

            ngDialog.open({ 
                template: '/static/templates/view-action-dialog.html', 
                width: '50%',
                controller: 'ActionView.ctrl',
                scope: $scope,
                onOpenCallback: function(){
                    $timeout(function(){
                        $('pre code').each(function(i, block) {
                            hljs.highlightBlock(block);
                        });
                    }, 100);
                }
            });
        });
    }
});

app.controller('ActionView.ctrl', function($scope, $timeout, ngDialog){
    $scope.copyURL = function(){
        // copy url to clipboard.
        (function (text) {
            var node = document.createElement('textarea');
            var selection = document.getSelection();
          
            node.textContent = text;
            document.body.appendChild(node);
          
            selection.removeAllRanges();
            node.select();
            document.execCommand('copy');
          
            selection.removeAllRanges();
            document.body.removeChild(node);
          })('http://localhost:8000/motty/base' + $scope.action.url);
          
          $.notify('The full url are copied.', {
              element: '#view-action-dialog',
          })
    }

    $scope.modify = function(){
        // I used temporarh hidden value due to trouble with ngDialog.
        $scope.closeThisDialog();
        $("#update_action_id").val($scope.action.id);

        ngDialog.open({ 
            template: '/static/templates/create-action-dialog.html', 
            controller: 'ActionEdit.ctrl'
        });
    }
});

app.controller('ActionEdit.ctrl', function($scope, $rootScope, Action){
    var id = $("#update_action_id").val();
    Action.get({id: id}, function(res){
        $scope.action = res;
    });

    $scope.save = function(){
        $scope.closeThisDialog();
        Action.update($scope.action, function(res){
            $rootScope.updateActions();
            $.notify('Successfully saved.');
        });
    };
});
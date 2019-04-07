var NetworkApp = angular.module("NetworkApp",[]);
NetworkApp.controller("userCtrl", function($scope){
    $scope.query = {};
    $scope.queryBy = '$';
    $scope.users = [
        {
            "name" : "Josephus",
            "gradDate" : "2020",
            "discipline" : "CS",
            "interests" : "Coding, Reading etc."
        },
        {
            "name" : "Alex",
            "gradDate" : "2020",
            "discipline" : "BBA",
            "interests" : "Socializing, Reading etc."
        },
        {
            "name" : "Alan",
            "gradDate" : "2021",
            "discipline" : "Civil",
            "interests" : "Skyscrapers, Reading etc."
        },
        {
            "name" : "Harris",
            "gradDate" : "2021",
            "discipline" : "EE",
            "interests" : "Circuits, Reading etc."
        },
        {
            "name" : "Nigel",
            "gradDate" : "2021",
            "discipline" : "Econ",
            "interests" : "Econ, Reading etc."
        },
    ];
    $scope.orderProp="name";
});

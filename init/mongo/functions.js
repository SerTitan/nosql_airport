db.system.js.save({
    _id: "topDestinations",
    value: function (limit) {
      return db.passengers.aggregate([
        { $group: { _id: "$flight_id", cnt: { $sum: 1 } } },
        { $sort: { cnt: -1 } },
        { $limit: limit }
      ]).toArray();
    }
  });
  
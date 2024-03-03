**HardQode_lms** Api for lms. Created with DRF


# Quick start

##### Download image from docker hub

---
```
docker pull sergeynaum/HardQode_lms:latest
```
---
##### Start the container by running the command
```
make docker_start
```
---
##### CONGRATULATIONS THE CONTAINER IS UP AND RUNNING AND THE API IS READY FOR TESTING_🚀

---
### Available methods for API requestsAvailable methods for API requests

API on the list of products available for purchase
```
curl http://127.0.0.1:8000/api/product-lst/
```

API with displaying the list of lessons for a particular product to which the user has access.

```
curl http://127.0.0.1:8000/api/product-lessons/{id}/
```

API for displaying product statistics.

```
curl http://127.0.0.1:8000/api/products/statistics/
```


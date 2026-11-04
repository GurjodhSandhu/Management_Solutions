import type { Truck } from "./types";

export const mockTruckPage = {
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "vin": "d12ee21eas1123124",
      "brand": "Freightliner",
      "make": "Cascadia 126",
      "plate": "5C8 90R",
      "year": 2022,
      "mileage": 43144,
      "truck_status": "AV",
      "truck_location": "AT"
    },
    {
      "id": 2,
      "vin": "3AKJHHDR6LSLM9281",
      "brand": "ford",
      "make": "T680",
      "plate": "a22bd2",
      "year": 2021,
      "mileage": 654200,
      "truck_status": "AV",
      "truck_location": "AT"
    },
    {
      "id": 3,
      "vin": "3HSDZAPR4KN685210",
      "brand": "Kenworth",
      "make": "pb231",
      "plate": "5C8 90R",
      "year": 2001,
      "mileage": 654200,
      "truck_status": "AV",
      "truck_location": "AT"
    }
  ] as Truck[],
}
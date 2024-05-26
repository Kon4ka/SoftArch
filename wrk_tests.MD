# Performance Test Comparison

| Metric          | Without Redis            | With Redis                |
|-----------------|--------------------------|---------------------------|
| Duration        | 30s                      | 30s                       |
| Threads         | 4                        | 4                         |
| Connections     | 100                      | 100                       |
| Avg Latency     | 108.71ms                 | 26.94ms                   |
| Latency Stdev   | 94.38ms                  | 10.90ms                   |
| Max Latency     | 1.02s                    | 352.78ms                  |
| Latency > Stdev | 90.35%                   | 93.09%                    |
| Avg Req/Sec     | 272.08                   | 940                       |
| Req/Sec Stdev   | 171.85                   | 121.89                    |
| Max Req/Sec     | 810                      | 1.22k                     |
| Req/Sec > Stdev | 68.96%                   | 72.08%                    |
| Total Requests  | 31,596                   | 113,138                   |
| Total Data Read | 7.05MB                   | 28.92MB                   |
| Requests/sec    | 1051.23                  | 3759.07                   |
| Transfer/sec    | 240.22KB                 | 960KB                     |



## Тест без Redis
baozorp@MacBook-Air Architectory % wrk -t4 -c100 -d30s 'http://localhost:8082/reports_read/664d1f9a75ff717441d0d5ca'
Running 30s test @ http://localhost:8082/reports_read/664d1f9a75ff717441d0d5ca
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   108.71ms   94.38ms   1.02s    90.35%
    Req/Sec   272.08    171.85   810.00     68.96%
  31596 requests in 30.06s, 7.05MB read
Requests/sec:   1051.23
Transfer/sec:    240.22KB

## Тест с redis
baozorp@MacBook-Air ~ %  wrk -t4 -c100 -d30s 'http://localhost:8082/reports_read/664d1f9a75ff717441d0d5ca'
Running 30s test @ http://localhost:8082/reports_read/664d1f9a75ff717441d0d5ca
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    26.94ms   10.90ms 352.78ms   93.09%
    Req/Sec     0.94k   121.89     1.22k    72.08%
  113138 requests in 30.10s, 28.92MB read
Requests/sec:   3759.07
Transfer/sec:      0.96MB
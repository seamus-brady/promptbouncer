
# Technical Overview: Parallel Processing for Scans in Prompt Bouncer

## Introduction

In the Prompt Bouncer project, parallel processing is utilized to efficiently run multiple threat scanners on an incoming prompt. This approach significantly reduces the time required to perform comprehensive threat assessments, enhancing the overall performance and responsiveness of the system.

## Threat Scanning Process

The threat scanning process involves several key components and steps, which are detailed below:

### Components

1. **ThreatScan Class**: Manages the execution of multiple threat scanners.
2. **AbstractThreatScanner**: An abstract base class that defines the interface for all threat scanners.
3. **Various Scanner Implementations**: Specific implementations of threat scanners (e.g., `CodeScanner`, `PromptInjectionScanner`, etc.).

### Steps

1. **Initialization**: The `ThreatScan` class is initialized with a set of available threat scanners.
2. **Thread Pool Creation**: A thread pool is created using Python's `concurrent.futures.ThreadPoolExecutor` to manage the execution of scanner tasks.
3. **Scanner Execution**: Each threat scanner is executed in parallel using the thread pool, with each scanner processing the incoming prompt independently.
4. **Result Collection**: The results (alarms) from each scanner are collected and aggregated.
5. **Threat Assessment**: The aggregated results are used to generate a comprehensive threat assessment.

## Detailed Workflow

### Initialization

When the `ThreatScan` class is instantiated, it initializes a dictionary of available threat scanners. Each scanner is an instance of a class that inherits from `AbstractThreatScanner`.

```python
class ThreatScan:
    def __init__(self) -> None:
        self._threat_scanners: Dict[str, Any] = {
            "CodeScanner": CodeScanner,
            "LanguageDetectionScanner": LanguageDetectionScanner,
            # Other scanners...
        }
```

### Thread Pool Creation

A thread pool is created to manage the parallel execution of scanner tasks. The `ThreadPoolExecutor` is configured with a maximum number of worker threads.

```python
def get_threadpool(self) -> ThreadPoolExecutor:
    return ThreadPoolExecutor(max_workers=self.MAX_WORKERS)
```

### Scanner Execution

The `run` method of the `ThreatScan` class submits each scanner task to the thread pool for parallel execution. The `run_text_scanner` function is used to run each scanner.

```python
def run(self, incoming_prompt: str) -> List[Alarm]:
    with self.get_threadpool() as executor:
        futures: List[Future] = []
        for _, scanner in self._threat_scanners.items():
            future = executor.submit(run_text_scanner, scanner, incoming_prompt)
            futures.append(future)
        completed_scans, _ = wait(futures)
        alarms = [future.result() for future in completed_scans]
    return alarms
```

### Result Collection

The `wait` function from `concurrent.futures` is used to wait for all scanner tasks to complete. The results are then collected from each `Future` object.

```python
completed_scans, _ = wait(futures)
alarms = [future.result() for future in completed_scans]
```

### Threat Assessment

The collected alarms are used to generate a comprehensive threat assessment. This involves calculating an overall threat level, confidence, and generating a recommendation based on the results of all scanners.

```python
assessment_score = Alarm.calculate_threat_level(...)
assessment_confidence = Alarm.calculate_overall_confidence(alarms)
assessment_description = Alarm.get_threat_description(assessment_score)
return ThreatAssessment(
    threats=alarms,
    assessment_score=assessment_score,
    assessment_description=assessment_description,
    assessment_confidence=assessment_confidence,
    recommendation=Bouncer.get_recommendation(assessment_score),
    time_taken_seconds=elapsed_time.__round__(2),
)
```

## Benefits of Parallel Processing

- **Efficiency**: Parallel processing allows multiple threat scanners to run simultaneously, significantly reducing the time required to perform a full threat assessment.
- **Scalability**: The system can easily scale to include additional threat scanners without a linear increase in assessment time.
- **Responsiveness**: Faster threat assessments improve the overall responsiveness of the system, providing timely insights and recommendations.

## Conclusion

By leveraging parallel processing, the Prompt Bouncer project enhances its threat assessment capabilities, delivering comprehensive and timely results. The use of Python's `concurrent.futures.ThreadPoolExecutor` allows the system to efficiently manage and execute multiple scanner tasks, making it a robust solution for real-time threat detection and assessment.

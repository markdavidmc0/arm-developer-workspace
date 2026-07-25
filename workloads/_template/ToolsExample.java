package com.arm.developer.workloads;

/**
 * Example Java MCP Tool definition for Arm workload auto-discovery.
 * Annotation processor emits build/mcp_schemas/java_tool_example.json sidecar.
 */
public class ToolsExample {

    public @interface McpTool {
        String name() default "";
        String description() default "";
    }

    @McpTool(
        name = "java_executorch_tensor_norm",
        description = "Performs FP32 Tensor Normalization for ExecuTorch mobile pipelines on Arm Cortex-X cores."
    )
    public static float[] javaExecuTorchTensorNorm(float[] inputData, float mean, float stdDev) {
        float[] normalized = new float[inputData.length];
        for (int i = 0; i < inputData.length; i++) {
            normalized[i] = (inputData[i] - mean) / stdDev;
        }
        return normalized;
    }

    public static void main(String[] args) {
        System.out.println("Java Arm Workload Template Initialized.");
    }
}

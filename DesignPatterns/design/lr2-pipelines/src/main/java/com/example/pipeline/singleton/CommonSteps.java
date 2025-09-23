package com.example.pipeline.singleton;

import com.example.pipeline.steps.TrimStep;
import com.example.pipeline.steps.LowercaseStep;

public class CommonSteps {
    public static final TrimStep TRIM = new TrimStep();
    public static final LowercaseStep LOWER = new LowercaseStep();

    private CommonSteps() {}
}

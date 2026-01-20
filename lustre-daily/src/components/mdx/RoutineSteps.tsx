import { ReactNode } from "react";

interface Step {
  title: string;
  description?: string;
  productAsin?: string;
}

interface RoutineStepsProps {
  title?: string;
  steps: Step[];
  children?: ReactNode;
}

export function RoutineSteps({ title, steps }: RoutineStepsProps) {
  return (
    <div className="my-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      {title && (
        <h4 className="mb-6 text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h4>
      )}
      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-4 top-0 h-full w-0.5 bg-gradient-to-b from-pink-400 to-purple-500" />

        {/* Steps */}
        <div className="space-y-6">
          {steps.map((step, index) => (
            <div key={index} className="relative flex items-start gap-4 pl-12">
              {/* Step number */}
              <div className="absolute left-0 flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-pink-500 to-purple-600 text-sm font-bold text-white">
                {index + 1}
              </div>

              {/* Step content */}
              <div className="flex-grow pt-0.5">
                <h5 className="font-medium text-gray-900 dark:text-white">
                  {step.title}
                </h5>
                {step.description && (
                  <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">
                    {step.description}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Alternative: Individual step component for more flexibility in MDX
interface StepProps {
  number: number;
  title: string;
  children?: ReactNode;
}

export function Step({ number, title, children }: StepProps) {
  return (
    <div className="relative flex items-start gap-4 py-4">
      <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-pink-500 to-purple-600 text-sm font-bold text-white">
        {number}
      </div>
      <div className="flex-grow">
        <h5 className="font-medium text-gray-900 dark:text-white">{title}</h5>
        {children && (
          <div className="mt-2 text-sm text-gray-600 dark:text-gray-300">
            {children}
          </div>
        )}
      </div>
    </div>
  );
}

export default RoutineSteps;

import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
  Box,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button,
  Typography,
  Stack,
  Tooltip,
} from '@mui/material';
import { FormStep2Data } from '../../types';

interface Step2FormProps {
  onSubmit: (data: FormStep2Data) => void;
  onBack: () => void;
  defaultValues?: Partial<FormStep2Data>;
  hasFirstDegree?: boolean;
  hasSecondDegree?: boolean;
}

const Step2Form: React.FC<Step2FormProps> = ({
  onSubmit,
  onBack,
  defaultValues,
  hasFirstDegree,
  hasSecondDegree,
}) => {
  const { control, handleSubmit } = useForm<FormStep2Data>({
    defaultValues: {
      degree: defaultValues?.degree || 1,
    },
  });

  const getDegreeDisabledState = (degree: number) => {
    if (degree === 1) return false;
    if (degree === 2) return hasFirstDegree;
    return hasFirstDegree || hasSecondDegree;
  };

  const getDegreeTooltip = (degree: number) => {
    if (degree === 2 && hasFirstDegree) {
      return "Cannot select second degree when there are first degree heirs";
    }
    if (degree === 3 && (hasFirstDegree || hasSecondDegree)) {
      return "Cannot select third degree when there are first or second degree heirs";
    }
    return "";
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ maxWidth: 600, mx: 'auto', p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Step 2: Inheritance Degree
      </Typography>

      <FormControl component="fieldset" margin="normal" fullWidth>
        <FormLabel>Select the applicable inheritance degree:</FormLabel>
        <Controller
          name="degree"
          control={control}
          rules={{ required: 'Please select a degree' }}
          render={({ field }) => (
            <RadioGroup {...field} value={field.value.toString()}>
              <FormControlLabel
                value="1"
                control={<Radio />}
                label={
                  <Box>
                    <Typography variant="subtitle1">First Degree</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Children and their descendants
                    </Typography>
                  </Box>
                }
              />
              <Tooltip title={getDegreeTooltip(2)} arrow>
                <FormControlLabel
                  value="2"
                  disabled={getDegreeDisabledState(2)}
                  control={<Radio />}
                  label={
                    <Box>
                      <Typography variant="subtitle1">Second Degree</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Parents and their descendants
                      </Typography>
                    </Box>
                  }
                />
              </Tooltip>
              <Tooltip title={getDegreeTooltip(3)} arrow>
                <FormControlLabel
                  value="3"
                  disabled={getDegreeDisabledState(3)}
                  control={<Radio />}
                  label={
                    <Box>
                      <Typography variant="subtitle1">Third Degree</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Grandparents and their descendants
                      </Typography>
                    </Box>
                  }
                />
              </Tooltip>
            </RadioGroup>
          )}
        />
      </FormControl>

      <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
        <Button
          variant="outlined"
          onClick={onBack}
          fullWidth
        >
          Back
        </Button>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
        >
          Next Step
        </Button>
      </Stack>
    </Box>
  );
};

export default Step2Form; 
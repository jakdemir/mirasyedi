import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
  Box,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button,
  Typography,
} from '@mui/material';
import { FormStep1Data } from '../../types';

interface Step1FormProps {
  onSubmit: (data: FormStep1Data) => void;
  defaultValues?: Partial<FormStep1Data>;
}

const Step1Form: React.FC<Step1FormProps> = ({ onSubmit, defaultValues }) => {
  const { control, handleSubmit, watch } = useForm<FormStep1Data>({
    defaultValues: {
      estate_value: defaultValues?.estate_value || 1000,
      has_spouse: defaultValues?.has_spouse ?? true,
      spouse_name: defaultValues?.spouse_name || '',
    },
  });

  const hasSpouse = watch('has_spouse');

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('tr-TR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ maxWidth: 600, mx: 'auto', p: 2 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Inheritance Calculator
      </Typography>

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Step 1: Initial Information
      </Typography>

      <Controller
        name="estate_value"
        control={control}
        rules={{ required: 'Estate value is required', min: { value: 0, message: 'Value must be positive' } }}
        render={({ field: { value, onChange, ...field }, fieldState: { error } }) => (
          <TextField
            {...field}
            value={value}
            onChange={(e) => {
              const val = e.target.value;
              onChange(val ? Number(val) : '');
            }}
            label="Total Estate Value"
            type="number"
            fullWidth
            margin="normal"
            error={!!error}
            helperText={error?.message || `Formatted: ${formatCurrency(value || 0)}`}
          />
        )}
      />

      <FormControl component="fieldset" margin="normal">
        <FormLabel>Is there a surviving spouse?</FormLabel>
        <Controller
          name="has_spouse"
          control={control}
          render={({ field }) => (
            <RadioGroup {...field} value={field.value.toString()}>
              <FormControlLabel
                value="true"
                control={<Radio />}
                label="Yes"
              />
              <FormControlLabel
                value="false"
                control={<Radio />}
                label="No"
              />
            </RadioGroup>
          )}
        />
      </FormControl>

      {hasSpouse && (
        <Controller
          name="spouse_name"
          control={control}
          rules={{ required: 'Spouse name is required' }}
          render={({ field, fieldState: { error } }) => (
            <TextField
              {...field}
              label="Spouse's Name"
              fullWidth
              margin="normal"
              error={!!error}
              helperText={error?.message}
            />
          )}
        />
      )}

      <Box sx={{ mt: 3 }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={hasSpouse && !watch('spouse_name')}
        >
          Next Step
        </Button>
      </Box>
    </Box>
  );
};

export default Step1Form; 
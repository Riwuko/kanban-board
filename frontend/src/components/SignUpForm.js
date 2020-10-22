import React from "react";
import { useForm } from "react-hook-form";
import {
  Button,
  CSSReset,
  Checkbox,
  Input,
  ThemeProvider,
} from "@chakra-ui/core";
import { ErrorMessage } from "@hookform/error-message";

const SignUpForm = () => {
  const { register, errors, watch, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <ThemeProvider>
      <CSSReset />
      <form onSubmit={handleSubmit(onSubmit)}>
        <Input
          name="email"
          ref={register({
            minLength: 8,
          })}
          placeholder="Email"
          required
        />

        <Input
          name="password"
          type="password"
          ref={register}
          placeholder="Password"
          required
        />

        <Input
          type="text"
          name="newPassword"
          type="password"
          ref={register({
            validate: (value) => value === watch("password"),
          })}
          placeholder="Repeat password"
          required
        />
        <ErrorMessage
          errors={errors}
          name="newPassword"
          message="Passwords don't match"
        />

        <Checkbox
          name="agreement"
          ref={register({
            required: "You have to accept the terms",
          })}
        >
          I agree to the Terms of Service
        </Checkbox>

        <Button type="submit">Send</Button>
      </form>
    </ThemeProvider>
  );
};

export default SignUpForm;

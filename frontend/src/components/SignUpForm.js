import React from "react";
import { useForm } from "react-hook-form";
import { Heading, Box, Flex, Input, Stack } from "@chakra-ui/core";
import githubLogo from "../styles/img/google_app_icon.png";
import googleLogo from "../styles/img/github_app_icon.png";
import { CheckboxForm, ButtonSubmit, ImageLogo, TextError } from "./CustomElements";

const SignUpPage = () => {
  return (
    <Flex
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      padding="1rem"
      width="100%"
    >
      <Heading marginBottom="3rem">Sign up</Heading>
      <Box width={["auto", "auto", "auto", "50vw", "22vw"]}>
        <SignUpForm />
        <SocialLogin />
      </Box>
    </Flex>
  );
};

const SignUpForm = () => {
  const { handleSubmit, register, errors, watch } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={5}>
        <Input
          name="email"
          type="text"
          ref={register}
          placeholder="Email"
          required
        />
        {errors.password && <TextError text="Password too short" />}
        <Input
          name="password"
          type={"password"}
          ref={register({
            minLength: 8,
            message: "Password too short",
          })}
          placeholder="Password"
          required
        />
        {errors.newPassword && <TextError text="Passwords don't match" />}
        <Input
          name="newPassword"
          type="password"
          ref={register({
            validate: (value) => value === watch("password"),
          })}
          placeholder="Repeat password"
          required
        />
        {errors.agreement && <TextError text={errors.agreement.message} />}
        <CheckboxForm
          name="agreement"
          variantColor="green"
          text="I agree to the Terms of Service"
          ref={register({
            required: "You have to accept the terms",
          })}
        />
        <ButtonSubmit type="submit" text="Submit" />
      </Stack>
    </form>
  );
};

const SocialLogin = () => {
  return (
    <Flex
      marginTop={["0", "0", "0", "1rem"]}
      justifyContent="space-around"
      width="100%"
    >
      <ImageLogo src={githubLogo} alt="Google Logo" text="Google Login" />
      <ImageLogo src={googleLogo} alt="Github Logo" text="Github Login" />
    </Flex>
  );
};

export default SignUpPage;
